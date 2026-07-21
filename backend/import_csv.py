"""
Importador de médicos via XLSX/CSV exportado do Veeva/Salesforce.

Uso:
    python import_csv.py alvos.xlsx
    python import_csv.py alvos.xlsx --dry-run     # simula sem gravar
    python import_csv.py alvos.xlsx --limpar      # apaga médicos sem reportes antes de importar

Formato esperado (exportação "Meus Alvos" do Veeva CRM):
    Licença | Nome da conta | Especialidade 1 | Linha de endereço 1 | Bairro | Cidade | Estado | CEP
"""

import argparse
import os
import re
import sys

# ─── MAPEAMENTO DE COLUNAS (exportação Veeva "Meus Alvos") ──────────────────
COLUNAS = {
    "licenca":       "Licença",
    "nome":          "Nome da conta",
    "especialidade": "Especialidade 1",
    "endereco":      "Linha de endereço 1",
    "bairro":        "Bairro",
    "cidade":        "Cidade",
    "uf":            "Estado",
    "cep":           "CEP",
    # Coluna opcional — presente em algumas linhas
    "esp_visita":    "Especialidade de Visitação",
}

DIAS_PADRAO    = "A confirmar"
HORARIO_PADRAO = "A confirmar"
# ────────────────────────────────────────────────────────────────────────────


def _extrair_nome(valor: str) -> str:
    """Extrai nome de =HYPERLINK("url", "Nome") ou devolve o valor direto."""
    if not valor:
        return ""
    m = re.search(r'HYPERLINK\s*\([^,]+,\s*"([^"]+)"', str(valor), re.IGNORECASE)
    if m:
        return m.group(1).strip()
    return str(valor).strip()


def _escolher_crm(licencas_raw: str, uf: str) -> str:
    """
    Licença pode ter vários CRMs separados por vírgula.
    Prefere o que começa com o UF da linha; senão usa o primeiro.
    Formato de saída: CRM-UF 0000000
    """
    if not licencas_raw:
        return ""
    partes = [p.strip() for p in str(licencas_raw).split(",") if p.strip()]
    if not partes:
        return ""

    # Tenta achar o CRM do estado da linha
    uf_upper = (uf or "").upper().strip()
    escolhido = partes[0]
    if uf_upper:
        for p in partes:
            if p.upper().startswith(uf_upper):
                escolhido = p
                break

    # Normaliza: "MG0004548" → "CRM-MG 0004548"
    m = re.match(r"([A-Z]{2})(\d+)", escolhido.upper())
    if m:
        return f"CRM-{m.group(1)} {m.group(2)}"
    return f"CRM {escolhido}"


def _get(row: dict, chave: str) -> str:
    col = COLUNAS.get(chave)
    if not col:
        return ""
    return str(row.get(col) or "").strip()


def _ler_arquivo(caminho: str) -> list[dict]:
    """Lê XLSX ou CSV e devolve lista de dicts."""
    ext = os.path.splitext(caminho)[1].lower()
    if ext in (".xlsx", ".xls"):
        import openpyxl
        wb = openpyxl.load_workbook(caminho)
        ws = wb.active
        headers = [cell.value for cell in next(ws.iter_rows(min_row=1, max_row=1))]
        return [
            {headers[i]: v for i, v in enumerate(row) if i < len(headers)}
            for row in ws.iter_rows(min_row=2, values_only=True)
        ]
    else:
        import csv
        with open(caminho, newline="", encoding="utf-8-sig") as f:
            return list(csv.DictReader(f))


def importar(caminho: str, dry_run: bool = False, limpar: bool = False):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from database import SessionLocal, engine
    from models import Base, Local, Medico

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        if limpar and not dry_run:
            sem_reportes = db.query(Medico).filter(Medico.total_reportes == 0).all()
            for m in sem_reportes:
                db.delete(m)
            db.commit()
            print(f"🗑  {len(sem_reportes)} médico(s) sem reportes removidos.\n")

        linhas = _ler_arquivo(caminho)
        print(f"📄 {len(linhas)} linha(s) encontrada(s) no arquivo.\n")

        inseridos = 0
        ignorados = 0
        erros     = 0

        for i, row in enumerate(linhas, start=2):
            uf           = _get(row, "uf")
            nome         = _extrair_nome(_get(row, "nome"))
            crm          = _escolher_crm(_get(row, "licenca"), uf)
            especialidade= _get(row, "especialidade") or _get(row, "esp_visita") or "Não informado"
            endereco     = _get(row, "endereco") or "Endereço não informado"
            bairro       = _get(row, "bairro") or None
            cidade       = _get(row, "cidade") or None
            cep          = _get(row, "cep") or None

            # Formata cidade com UF: "Belo Horizonte (MG)"
            cidade_fmt = f"{cidade} ({uf})" if cidade and uf else cidade

            if not nome or not crm:
                print(f"  ⚠  Linha {i}: nome ou CRM ausente — ignorada.")
                erros += 1
                continue

            existente = db.query(Medico).filter(Medico.crm == crm).first()
            if existente:
                ignorados += 1
                continue

            if not dry_run:
                medico = Medico(nome=nome, crm=crm, especialidade=especialidade)
                db.add(medico)
                db.flush()
                db.add(Local(
                    medico_id=medico.id,
                    endereco=endereco,
                    bairro=bairro,
                    cidade=cidade_fmt,
                    dias=DIAS_PADRAO,
                    horario=HORARIO_PADRAO,
                    verificado=False,
                ))

            inseridos += 1

        if not dry_run:
            db.commit()

        modo = "[DRY-RUN] " if dry_run else ""
        print(f"{modo}Importação concluída:")
        print(f"  ✅  {inseridos} médico(s) inserido(s)")
        print(f"  ⏭  {ignorados} ignorado(s) — CRM já existe no banco")
        print(f"  ❌  {erros} linha(s) com erro de validação")

    except Exception as e:
        db.rollback()
        print(f"\n❌ Erro: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Importa médicos de XLSX/CSV Veeva")
    parser.add_argument("arquivo", help="Caminho para o arquivo (.xlsx ou .csv)")
    parser.add_argument("--dry-run", action="store_true", help="Simula sem gravar no banco")
    parser.add_argument("--limpar", action="store_true", help="Remove médicos sem reportes antes de importar")
    args = parser.parse_args()

    if not os.path.exists(args.arquivo):
        print(f"❌ Arquivo não encontrado: {args.arquivo}")
        sys.exit(1)

    importar(args.arquivo, dry_run=args.dry_run, limpar=args.limpar)
