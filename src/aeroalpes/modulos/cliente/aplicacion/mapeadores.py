from aeroalpes.modulos.cliente.aplicacion.dto import ClienteDTO, MetodoPagoDTO
from aeroalpes.modulos.cliente.dominio.entidades import ClienteNatural as Cliente
from aeroalpes.modulos.cliente.dominio.objetos_valor import Email, Cedula, TipoMetodoPago

class MapeadorClienteDTOJson:
    def externo_a_dto(self, data: dict) -> ClienteDTO:
        return ClienteDTO(
            nombre=data.get('nombre'),
            apellido=data.get('apellido'),
            email=data.get('email'),
            cedula=data.get('cedula')
        )

    def dto_a_externo(self, dto: ClienteDTO) -> dict:
        return {
            'nombre': dto.nombre,
            'apellido': dto.apellido,
            'email': dto.email,
            'cedula': dto.cedula
        }

    def dto_a_externo(self, dto: ClienteDTO) -> dict:
        return dto.__dict__


class MapeadorMetodoPagoDTOJson:
    def externo_a_dto(self, data: dict) -> MetodoPagoDTO:
        return MetodoPagoDTO(
            tipo=data.get('tipo'),
            nombre=data.get('nombre'),
            token=data.get('token')
        )

    def dto_a_externo(self, dto: MetodoPagoDTO) -> dict:
        return {
            'tipo': dto.tipo,
            'nombre': dto.nombre,
            'token': dto.token
        }


