"""
Lógica de parsing de XLSX/CSV Veeva compartilhada entre o CLI e a API.
"""

import io
import re

COLUNAS = {
    "licenca":       "Licença",
    "nome":          "Nome da conta",
    "especialidade": "Especialidade 1",
    "endereco":      "Linha de endereço 1",
    "bairro":        "Bairro",
    "cidade":        "Cidade",
    "uf":            "Estado",
    "cep":           "CEP",
    "esp_visita":    "Especialidade de Visitação",
}

DIAS_PADRAO    = "A confirmar"
HORARIO_PADRAO = "A confirmar"


def _get(row: dict, chave: str) -> str:
    col = COLUNAS.get(chave)
    if not col:
        return ""
    return str(row.get(col) or "").strip()


def _extrair_nome(valor: str) -> str:
    if not valor:
        return ""
    m = re.search(r'HYPERLINK\s*\([^,]+,\s*"([^"]+)"', str(valor), re.IGNORECASE)
    return m.group(1).strip() if m else str(valor).strip()


def _escolher_crm(licencas_raw: str, uf: str) -> str:
    if not licencas_raw:
        return ""
    partes = [p.strip() for p in str(licencas_raw).split(",") if p.strip()]
    if not partes:
        return ""
    uf_upper = (uf or "").upper().strip()
    escolhido = partes[0]
    if uf_upper:
        for p in partes:
            if p.upper().startswith(uf_upper):
                escolhido = p
                break
    m = re.match(r"([A-Z]{2})(\d+)", escolhido.upper())
    return f"CRM-{m.group(1)} {m.group(2)}" if m else f"CRM {escolhido}"


def _linhas_de_sheet(ws) -> list[dict]:
    headers = [cell.value for cell in next(ws.iter_rows(min_row=1, max_row=1))]
    return [
        {headers[i]: v for i, v in enumerate(row) if i < len(headers)}
        for row in ws.iter_rows(min_row=2, values_only=True)
    ]


def ler_xlsx_bytes(conteudo: bytes) -> list[dict]:
    import openpyxl
    wb = openpyxl.load_workbook(io.BytesIO(conteudo))
    return _linhas_de_sheet(wb.active)


def ler_arquivo(caminho: str) -> list[dict]:
    import os
    ext = os.path.splitext(caminho)[1].lower()
    if ext in (".xlsx", ".xls"):
        import openpyxl
        wb = openpyxl.load_workbook(caminho)
        return _linhas_de_sheet(wb.active)
    else:
        import csv
        with open(caminho, newline="", encoding="utf-8-sig") as f:
            return list(csv.DictReader(f))


def parsear_medico(row: dict) -> dict | None:
    """Converte uma linha do arquivo em dict de médico. Retorna None se inválida."""
    uf           = _get(row, "uf")
    nome         = _extrair_nome(_get(row, "nome"))
    crm          = _escolher_crm(_get(row, "licenca"), uf)
    especialidade= _get(row, "especialidade") or _get(row, "esp_visita") or "Não informado"
    endereco     = _get(row, "endereco") or "Endereço não informado"
    bairro       = _get(row, "bairro") or None
    cidade_raw   = _get(row, "cidade") or None
    cidade       = f"{cidade_raw} ({uf})" if cidade_raw and uf else cidade_raw

    if not nome or not crm:
        return None

    return {
        "nome": nome,
        "crm": crm,
        "especialidade": especialidade,
        "endereco": endereco,
        "bairro": bairro,
        "cidade": cidade,
    }
