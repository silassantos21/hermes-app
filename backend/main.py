import asyncio
import json
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from pathlib import Path

import socketio
from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

import importador
import models
import schemas
from database import SessionLocal, engine, get_db
from schemas import ConfirmarCreate, LocalCreate
from seed import seed_database

# ── Banco: cria tabelas e seed inicial ───────────────────
models.Base.metadata.create_all(bind=engine)


def _migrar_colunas():
    """Adiciona colunas que podem não existir em bancos criados antes da migração."""
    from sqlalchemy import text
    migracoes = [
        "ALTER TABLE locais ADD COLUMN IF NOT EXISTS bairro VARCHAR",
        "ALTER TABLE locais ADD COLUMN IF NOT EXISTS cidade VARCHAR",
        "ALTER TABLE locais_pendentes ADD COLUMN IF NOT EXISTS bairro VARCHAR",
        "ALTER TABLE locais_pendentes ADD COLUMN IF NOT EXISTS cidade VARCHAR",
    ]
    with engine.connect() as conn:
        for sql in migracoes:
            try:
                conn.execute(text(sql))
            except Exception:
                pass
        conn.commit()


_migrar_colunas()


def _init_db():
    db = SessionLocal()
    try:
        if db.query(models.Medico).count() == 0:
            seed_database(db)
    finally:
        db.close()


_init_db()

# ── Socket.io (definido antes do lifespan para poder usar no loop) ────
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")


async def _expirar_status_loop():
    while True:
        await asyncio.sleep(30 * 60)
        db = SessionLocal()
        try:
            limite = datetime.utcnow() - timedelta(hours=12)
            medicos = (
                db.query(models.Medico)
                .filter(models.Medico.updated_at < limite, models.Medico.status != "indisponivel")
                .all()
            )
            for m in medicos:
                m.status = "indisponivel"
                await sio.emit("status_update", {"medicoId": m.id, "status": "indisponivel", "reportadoPor": ""})
            if medicos:
                db.commit()
        finally:
            db.close()


@asynccontextmanager
async def lifespan(app):
    asyncio.create_task(_expirar_status_loop())
    yield


# ── FastAPI ───────────────────────────────────────────────
fastapi_app = FastAPI(title="Hermes API", lifespan=lifespan)
fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Socket.io (ASGI wrapper sobre o FastAPI) ──────────────
app = socketio.ASGIApp(sio, other_asgi_app=fastapi_app)


@sio.event
async def connect(sid, environ):
    print(f"[ws] conectado:    {sid}")


@sio.event
async def disconnect(sid):
    print(f"[ws] desconectado: {sid}")


# ── Helpers de serialização ───────────────────────────────
def _medico_dict(m: models.Medico) -> dict:
    return {
        "id": m.id,
        "nome": m.nome,
        "crm": m.crm,
        "especialidade": m.especialidade,
        "status": m.status,
        "ultimoReporte": m.ultimo_reporte,
        "reportadoPor": m.reportado_por,
        "totalReportes": m.total_reportes,
        "locais": [
            {
                "id": l.id,
                "endereco": l.endereco,
                "dias": l.dias,
                "horario": l.horario,
                "verificado": l.verificado,
                "diasVerif": l.dias_verif,
                "telefone": l.telefone,
                "secretaria": l.secretaria,
                "bairro": l.bairro,
                "cidade": l.cidade,
                "adicionadoEm": _tempo_relativo(l.created_at) if l.created_at else None,
            }
            for l in sorted(m.locais, key=lambda x: x.created_at or datetime.min, reverse=True)
        ],
        "locaisPendentes": [
            {
                "id": lp.id,
                "endereco": lp.endereco,
                "dias": lp.dias,
                "horario": lp.horario,
                "telefone": lp.telefone,
                "secretaria": lp.secretaria,
                "bairro": lp.bairro,
                "cidade": lp.cidade,
                "propostoPor": lp.proposto_por,
                "confirmacoes": len(json.loads(lp.confirmados or "[]")),
                "confirmados": json.loads(lp.confirmados or "[]"),
                "threshold": lp.threshold,
            }
            for lp in m.locais_pendentes
        ],
    }


def _tempo_relativo(dt: datetime) -> str:
    diff = (datetime.utcnow() - dt).total_seconds()
    if diff < 60:
        return "agora"
    if diff < 3600:
        return f"{int(diff / 60)} min atrás"
    if diff < 86400:
        return f"{int(diff / 3600)}h atrás"
    return f"{int(diff / 86400)}d atrás"


def _reporte_dict(r: models.Reporte) -> dict:
    return {
        "id": r.id,
        "usuario": r.usuario_apelido,
        "medico": r.medico_nome,
        "acao": r.opcao_label,
        "tempo": _tempo_relativo(r.created_at),
        "status": r.opcao_id,
        "xp": r.xp,
    }


# ── Rotas da API ──────────────────────────────────────────
@fastapi_app.get("/api/medicos")
def listar_medicos(db: Session = Depends(get_db)):
    return [_medico_dict(m) for m in db.query(models.Medico).all()]


@fastapi_app.post("/api/reportes")
async def criar_reporte(body: schemas.ReporteCreate, db: Session = Depends(get_db)):
    medico = db.query(models.Medico).filter(models.Medico.id == body.medico_id).first()
    if not medico:
        raise HTTPException(status_code=404, detail="Médico não encontrado")

    if body.opcao_id not in ("endereco", "nao_trabalha"):
        medico.status = body.opcao_id
        medico.ultimo_reporte = "agora"
        medico.reportado_por = body.usuario_apelido
        medico.total_reportes += 1
        medico.updated_at = datetime.utcnow()

    reporte = models.Reporte(
        medico_id=body.medico_id,
        medico_nome=medico.nome,
        usuario_apelido=body.usuario_apelido,
        opcao_id=body.opcao_id,
        opcao_label=body.opcao_label,
        xp=body.xp,
    )
    db.add(reporte)

    usuario = db.query(models.Usuario).filter(
        models.Usuario.apelido == body.usuario_apelido
    ).first()
    if usuario:
        usuario.xp_total += body.xp

    db.commit()
    db.refresh(reporte)

    await sio.emit("status_update", {
        "medicoId": medico.id,
        "status": medico.status,
        "reportadoPor": body.usuario_apelido,
    })
    await sio.emit("novo_reporte", _reporte_dict(reporte))

    return {"ok": True, "id": reporte.id}


@fastapi_app.post("/api/medicos/{medico_id}/locais")
async def adicionar_local(medico_id: int, body: LocalCreate, db: Session = Depends(get_db)):
    medico = db.query(models.Medico).filter(models.Medico.id == medico_id).first()
    if not medico:
        raise HTTPException(status_code=404, detail="Médico não encontrado")

    usuario = db.query(models.Usuario).filter(models.Usuario.apelido == body.usuario_apelido).first()
    xp_usuario = usuario.xp_total if usuario else 0

    if xp_usuario >= 200:
        local = models.Local(
            medico_id=medico_id,
            endereco=body.endereco,
            dias=body.dias,
            horario=body.horario,
            verificado=True,
            dias_verif=0,
            telefone=body.telefone,
            secretaria=body.secretaria,
            bairro=body.bairro,
            cidade=body.cidade,
        )
        db.add(local)
        db.commit()
        db.refresh(local)

        await sio.emit("local_adicionado", {
            "medicoId": medico_id,
            "local": {
                "id": local.id,
                "endereco": local.endereco,
                "dias": local.dias,
                "horario": local.horario,
                "verificado": local.verificado,
                "diasVerif": local.dias_verif,
                "telefone": local.telefone,
                "secretaria": local.secretaria,
                "bairro": local.bairro,
                "cidade": local.cidade,
                "adicionadoEm": "agora",
            },
        })
        return {"ok": True, "pendente": False, "id": local.id}
    else:
        pendente = models.LocalPendente(
            medico_id=medico_id,
            endereco=body.endereco,
            dias=body.dias,
            horario=body.horario,
            telefone=body.telefone,
            secretaria=body.secretaria,
            bairro=body.bairro,
            cidade=body.cidade,
            proposto_por=body.usuario_apelido,
            confirmados="[]",
            threshold=3,
        )
        db.add(pendente)
        db.commit()
        db.refresh(pendente)

        await sio.emit("local_pendente_criado", {
            "medicoId": medico_id,
            "pendente": {
                "id": pendente.id,
                "endereco": pendente.endereco,
                "dias": pendente.dias,
                "horario": pendente.horario,
                "telefone": pendente.telefone,
                "secretaria": pendente.secretaria,
                "bairro": pendente.bairro,
                "cidade": pendente.cidade,
                "propostoPor": pendente.proposto_por,
                "confirmacoes": 0,
                "confirmados": [],
                "threshold": pendente.threshold,
            },
        })
        return {"ok": True, "pendente": True, "id": pendente.id}


@fastapi_app.post("/api/locais-pendentes/{pendente_id}/confirmar")
async def confirmar_local_pendente(pendente_id: int, body: ConfirmarCreate, db: Session = Depends(get_db)):
    pendente = db.query(models.LocalPendente).filter(models.LocalPendente.id == pendente_id).first()
    if not pendente:
        raise HTTPException(status_code=404, detail="Local pendente não encontrado")

    confirmados = json.loads(pendente.confirmados or "[]")

    if body.apelido == pendente.proposto_por:
        raise HTTPException(status_code=400, detail="Não pode confirmar a própria sugestão")
    if body.apelido in confirmados:
        raise HTTPException(status_code=400, detail="Já confirmou este local")

    confirmados.append(body.apelido)
    pendente.confirmados = json.dumps(confirmados)
    medico_id = pendente.medico_id

    if len(confirmados) >= pendente.threshold:
        local = models.Local(
            medico_id=medico_id,
            endereco=pendente.endereco,
            dias=pendente.dias,
            horario=pendente.horario,
            verificado=True,
            dias_verif=0,
            telefone=pendente.telefone,
            secretaria=pendente.secretaria,
            bairro=pendente.bairro,
            cidade=pendente.cidade,
        )
        db.add(local)
        pendente_id_emit = pendente.id
        db.delete(pendente)
        db.commit()
        db.refresh(local)

        await sio.emit("local_adicionado", {
            "medicoId": medico_id,
            "local": {
                "id": local.id,
                "endereco": local.endereco,
                "dias": local.dias,
                "horario": local.horario,
                "verificado": local.verificado,
                "diasVerif": local.dias_verif,
                "telefone": local.telefone,
                "secretaria": local.secretaria,
                "bairro": local.bairro,
                "cidade": local.cidade,
                "adicionadoEm": "agora",
            },
        })
        await sio.emit("local_pendente_promovido", {
            "medicoId": medico_id,
            "pendenteId": pendente_id_emit,
            "medicoNome": medico.nome,
            "endereco": local.endereco,
        })
    else:
        db.commit()
        await sio.emit("confirmacao_adicionada", {
            "medicoId": medico_id,
            "pendenteId": pendente_id,
            "confirmacoes": len(confirmados),
            "confirmados": confirmados,
            "threshold": pendente.threshold,
        })

    return {"ok": True}


@fastapi_app.delete("/api/reportes/{reporte_id}")
async def desfazer_reporte(reporte_id: int, apelido: str, db: Session = Depends(get_db)):
    reporte = db.query(models.Reporte).filter(models.Reporte.id == reporte_id).first()
    if not reporte:
        raise HTTPException(status_code=404, detail="Reporte não encontrado")
    if reporte.usuario_apelido != apelido:
        raise HTTPException(status_code=403, detail="Não é seu reporte")

    medico = db.query(models.Medico).filter(models.Medico.id == reporte.medico_id).first()

    usuario = db.query(models.Usuario).filter(models.Usuario.apelido == apelido).first()
    if usuario:
        usuario.xp_total = max(0, usuario.xp_total - reporte.xp)

    emite_status = reporte.opcao_id not in ("endereco", "nao_trabalha")
    medico_id_emit = reporte.medico_id

    if emite_status and medico:
        medico.total_reportes = max(0, medico.total_reportes - 1)
        reporte_anterior = (
            db.query(models.Reporte)
            .filter(
                models.Reporte.medico_id == reporte.medico_id,
                models.Reporte.id != reporte.id,
                models.Reporte.opcao_id.notin_(["endereco", "nao_trabalha"]),
            )
            .order_by(models.Reporte.created_at.desc())
            .first()
        )
        if reporte_anterior:
            medico.status = reporte_anterior.opcao_id
            medico.reportado_por = reporte_anterior.usuario_apelido
            medico.ultimo_reporte = _tempo_relativo(reporte_anterior.created_at)
        else:
            medico.status = "indisponivel"
            medico.reportado_por = ""
            medico.ultimo_reporte = "sem informação"

    reporte_id_emit = reporte.id
    db.delete(reporte)
    db.commit()

    if emite_status and medico:
        await sio.emit("status_update", {
            "medicoId": medico.id,
            "status": medico.status,
            "reportadoPor": medico.reportado_por,
        })
    await sio.emit("reporte_desfeito", {"reporteId": reporte_id_emit})
    return {"ok": True}


@fastapi_app.get("/api/feed")
def listar_feed(db: Session = Depends(get_db)):
    reportes = (
        db.query(models.Reporte)
        .order_by(models.Reporte.created_at.desc())
        .limit(20)
        .all()
    )
    return [_reporte_dict(r) for r in reportes]


@fastapi_app.get("/api/ranking")
def listar_ranking(db: Session = Depends(get_db)):
    usuarios = db.query(models.Usuario).order_by(models.Usuario.xp_total.desc()).limit(20).all()
    result = []
    for i, u in enumerate(usuarios):
        total_rep = db.query(models.Reporte).filter(models.Reporte.usuario_apelido == u.apelido).count()
        result.append({"posicao": i + 1, "apelido": u.apelido, "xp": u.xp_total, "reportes": total_rep})
    return result


@fastapi_app.get("/api/usuarios/{apelido}")
def buscar_usuario(apelido: str, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.apelido == apelido).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    total_rep = db.query(models.Reporte).filter(models.Reporte.usuario_apelido == apelido).count()
    posicao = db.query(models.Usuario).filter(models.Usuario.xp_total > usuario.xp_total).count() + 1
    return {"apelido": usuario.apelido, "xp": usuario.xp_total, "reportes": total_rep, "posicao": posicao}


@fastapi_app.post("/api/usuarios")
def criar_ou_buscar_usuario(body: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(
        models.Usuario.apelido == body.apelido
    ).first()
    if not usuario:
        usuario = models.Usuario(apelido=body.apelido, xp_total=0)
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
    return {"id": usuario.id, "apelido": usuario.apelido, "xp_total": usuario.xp_total}


# ── Admin: importação de médicos ──────────────────────────
@fastapi_app.post("/api/admin/preview-importacao")
async def preview_importacao(arquivo: UploadFile = File(...), db: Session = Depends(get_db)):
    conteudo = await arquivo.read()
    try:
        linhas = importador.ler_xlsx_bytes(conteudo)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao ler arquivo: {e}")

    crms_existentes = {m.crm for m in db.query(models.Medico.crm).all()}

    medicos = []
    for row in linhas:
        data = importador.parsear_medico(row)
        if not data:
            continue
        data["status"] = "duplicado" if data["crm"] in crms_existentes else "novo"
        medicos.append(data)

    novos      = sum(1 for m in medicos if m["status"] == "novo")
    duplicados = sum(1 for m in medicos if m["status"] == "duplicado")
    return {"total": len(medicos), "novos": novos, "duplicados": duplicados, "medicos": medicos}


@fastapi_app.post("/api/admin/importar")
async def importar_medicos(arquivo: UploadFile = File(...), db: Session = Depends(get_db)):
    conteudo = await arquivo.read()
    try:
        linhas = importador.ler_xlsx_bytes(conteudo)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao ler arquivo: {e}")

    crms_existentes = {m.crm for m in db.query(models.Medico.crm).all()}
    inseridos = ignorados = erros = 0

    for row in linhas:
        data = importador.parsear_medico(row)
        if not data:
            erros += 1
            continue
        if data["crm"] in crms_existentes:
            ignorados += 1
            continue
        medico = models.Medico(nome=data["nome"], crm=data["crm"], especialidade=data["especialidade"])
        db.add(medico)
        db.flush()
        db.add(models.Local(
            medico_id=medico.id,
            endereco=data["endereco"],
            bairro=data["bairro"],
            cidade=data["cidade"],
            dias="A confirmar",
            horario="A confirmar",
            verificado=False,
        ))
        crms_existentes.add(data["crm"])
        inseridos += 1

    db.commit()
    return {"inseridos": inseridos, "ignorados": ignorados, "erros": erros}


# ── Arquivos estáticos — deve ficar por último ────────────
_static_dir = Path(__file__).parent.parent / "src"
if _static_dir.exists():
    fastapi_app.mount("/", StaticFiles(directory=str(_static_dir), html=True), name="static")
