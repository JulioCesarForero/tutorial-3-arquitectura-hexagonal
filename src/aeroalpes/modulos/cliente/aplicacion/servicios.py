import uuid

from aeroalpes.modulos.cliente.dominio.entidades import ClienteNatural as Cliente
from aeroalpes.modulos.cliente.dominio.objetos_valor import Email, Cedula, MetodoPago, TipoMetodoPago
from aeroalpes.modulos.cliente.infraestructura.repositorios import RepositorioClienteSQLite
from aeroalpes.modulos.cliente.aplicacion.dto import ClienteDTO, MetodoPagoDTO

class ServicioCliente:
    def __init__(self):
        self.repo = RepositorioClienteSQLite()

    def registrar_usuario(self, cliente_dto: ClienteDTO) -> ClienteDTO:
        # Crear objetos de valor a partir de los datos del DTO
        email_obj = Email(cliente_dto.email)
        cedula_obj = Cedula(cliente_dto.cedula)
        # Usar los objetos validados en lugar de los valores sin procesar
        cliente = Cliente(cliente_dto.nombre, cliente_dto.apellido, email_obj, cedula_obj)
        self.repo.agregar(cliente)
        return cliente_dto

    def agregar_metodo_pago(self, cliente_id: str, metodo_pago_dto: MetodoPagoDTO) -> dict:
        cliente = self.repo.obtener_por_id(cliente_id)
        if cliente is None:
            raise ValueError("Cliente no encontrado.")
        token = metodo_pago_dto.token if metodo_pago_dto.token else str(uuid.uuid4())
        tipo = TipoMetodoPago(metodo_pago_dto.tipo)
        metodo_pago = MetodoPago(tipo, metodo_pago_dto.nombre, token)
        cliente.agregar_metodo_pago(metodo_pago)
        self.repo.actualizar(cliente)
        return {"mensaje": "Método de pago agregado", "token": token}

    def modificar_metodo_pago(self, cliente_id: str, metodo_pago_dto: MetodoPagoDTO) -> dict:
        cliente = self.repo.obtener_por_id(cliente_id)
        if cliente is None:
            raise ValueError("Cliente no encontrado.")
        if not metodo_pago_dto.token:
            raise ValueError("Token del método de pago requerido para modificar.")
        cliente.modificar_metodo_pago(metodo_pago_dto.token, metodo_pago_dto.nombre)
        self.repo.actualizar(cliente)
        return {"mensaje": "Método de pago modificado"}

    def eliminar_metodo_pago(self, cliente_id: str, token: str) -> dict:
        cliente = self.repo.obtener_por_id(cliente_id)
        if cliente is None:
            raise ValueError("Cliente no encontrado.")
        cliente.eliminar_metodo_pago(token)
        self.repo.actualizar(cliente)
        return {"mensaje": "Método de pago eliminado"}
