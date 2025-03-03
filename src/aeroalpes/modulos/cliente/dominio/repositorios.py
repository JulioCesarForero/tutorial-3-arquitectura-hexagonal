from abc import ABC, abstractmethod
# from aeroalpes.modulos.cliente.dominio.entidades import Cliente
from aeroalpes.modulos.cliente.dominio.entidades import ClienteNatural as Cliente


class RepositorioCliente(ABC):
    @abstractmethod
    def agregar(self, cliente: Cliente):
        pass

    @abstractmethod
    def actualizar(self, cliente: Cliente):
        pass

    @abstractmethod
    def eliminar(self, cliente: Cliente):
        pass

    @abstractmethod
    def obtener_por_id(self, id: str) -> Cliente:
        pass
