"""
Importador CLI de médicos via XLSX/CSV (exportação Veeva/Salesforce).

Uso:
    python import_csv.py alvos.xlsx
    python import_csv.py alvos.xlsx --dry-run
    python import_csv.py alvos.xlsx --limpar
"""

import argparse
import os
import sys


def importar(caminho: str, dry_run: bool = False, limpar: bool = False):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from database import SessionLocal, engine
    from importador import ler_arquivo, parsear_medico
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

        linhas = ler_arquivo(caminho)
        print(f"📄 {len(linhas)} linha(s) encontrada(s) no arquivo.\n")

        inseridos = ignorados = erros = 0

        for i, row in enumerate(linhas, start=2):
            medico_data = parsear_medico(row)
            if not medico_data:
                print(f"  ⚠  Linha {i}: nome ou CRM ausente — ignorada.")
                erros += 1
                continue

            if db.query(Medico).filter(Medico.crm == medico_data["crm"]).first():
                ignorados += 1
                continue

            if not dry_run:
                m = Medico(nome=medico_data["nome"], crm=medico_data["crm"], especialidade=medico_data["especialidade"])
                db.add(m)
                db.flush()
                db.add(Local(
                    medico_id=m.id,
                    endereco=medico_data["endereco"],
                    bairro=medico_data["bairro"],
                    cidade=medico_data["cidade"],
                    dias="A confirmar",
                    horario="A confirmar",
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
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limpar", action="store_true")
    args = parser.parse_args()

    if not os.path.exists(args.arquivo):
        print(f"❌ Arquivo não encontrado: {args.arquivo}")
        sys.exit(1)

    importar(args.arquivo, dry_run=args.dry_run, limpar=args.limpar)
