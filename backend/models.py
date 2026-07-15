from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Medico(Base):
    __tablename__ = "medicos"

    id             = Column(Integer, primary_key=True, index=True)
    nome           = Column(String, nullable=False)
    crm            = Column(String, nullable=False, unique=True)
    especialidade  = Column(String, nullable=False)
    status         = Column(String, default="indisponivel")
    ultimo_reporte = Column(String, default="sem informação")
    reportado_por  = Column(String, default="")
    total_reportes = Column(Integer, default=0)
    updated_at     = Column(DateTime, default=datetime.utcnow)

    locais           = relationship("Local",         back_populates="medico", cascade="all, delete-orphan")
    locais_pendentes = relationship("LocalPendente", back_populates="medico", cascade="all, delete-orphan")


class Local(Base):
    __tablename__ = "locais"

    id         = Column(Integer, primary_key=True, index=True)
    medico_id  = Column(Integer, ForeignKey("medicos.id"), nullable=False)
    endereco   = Column(String, nullable=False)
    dias       = Column(String, nullable=False)
    horario    = Column(String, nullable=False)
    verificado = Column(Boolean, default=False)
    dias_verif = Column(Integer, default=0)
    telefone   = Column(String, nullable=True)
    secretaria = Column(String, nullable=True)
    bairro     = Column(String, nullable=True)
    cidade     = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    medico = relationship("Medico", back_populates="locais")


class LocalPendente(Base):
    __tablename__ = "locais_pendentes"

    id           = Column(Integer, primary_key=True, index=True)
    medico_id    = Column(Integer, ForeignKey("medicos.id"), nullable=False)
    endereco     = Column(String, nullable=False)
    dias         = Column(String, nullable=False)
    horario      = Column(String, nullable=False)
    telefone     = Column(String, nullable=True)
    secretaria   = Column(String, nullable=True)
    bairro       = Column(String, nullable=True)
    cidade       = Column(String, nullable=True)
    proposto_por = Column(String, nullable=False)
    confirmados  = Column(String, default="[]")  # JSON list de apelidos
    threshold    = Column(Integer, default=3)
    created_at   = Column(DateTime, default=datetime.utcnow)

    medico = relationship("Medico", back_populates="locais_pendentes")


class Reporte(Base):
    __tablename__ = "reportes"

    id              = Column(Integer, primary_key=True, index=True)
    medico_id       = Column(Integer, ForeignKey("medicos.id"), nullable=False)
    medico_nome     = Column(String, nullable=False)
    usuario_apelido = Column(String, nullable=False)
    opcao_id        = Column(String, nullable=False)
    opcao_label     = Column(String, nullable=False)
    xp              = Column(Integer, nullable=False)
    created_at      = Column(DateTime, default=datetime.utcnow)


class Usuario(Base):
    __tablename__ = "usuarios"

    id         = Column(Integer, primary_key=True, index=True)
    apelido    = Column(String, nullable=False, unique=True)
    xp_total   = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
