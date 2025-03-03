from dataclasses import dataclass, field
from aeroalpes.seedwork.aplicacion.dto import DTO

@dataclass(frozen=True)
class ClienteDTO(DTO):
    nombre: str
    apellido: str
    email: str
    cedula: str

@dataclass(frozen=True)
class MetodoPagoDTO(DTO):
    tipo: str
    nombre: str
    token: str = field(default=None)
