from pydantic import BaseModel


class ReporteCreate(BaseModel):
    medico_id: int
    usuario_apelido: str
    opcao_id: str
    opcao_label: str
    xp: int


class UsuarioCreate(BaseModel):
    apelido: str


class LocalCreate(BaseModel):
    endereco: str
    dias: str
    horario: str
    telefone: str | None = None
    secretaria: str | None = None
