"""Entidades del dominio de cliente
En este archivo usted encontrará las entidades del dominio de cliente
"""

from datetime import datetime
from typing import List
from dataclasses import dataclass, field
from aeroalpes.seedwork.dominio.entidades import Entidad
from .objetos_valor import Nombre, Email, Cedula, Rut, MetodoPago

@dataclass(kw_only=True)
class Usuario(Entidad):
    nombre: Nombre
    email: Email

@dataclass(kw_only=True)
class ClienteNatural(Usuario):
    cedula: Cedula
    fecha_nacimiento: datetime = field(default_factory=datetime)
    metodos_pago: List[MetodoPago] = field(default_factory=list)

    def agregar_metodo_pago(self, metodo: MetodoPago):
        self.metodos_pago.append(metodo)

    def modificar_metodo_pago(self, token: str, nuevo_nombre: str):
        for mp in self.metodos_pago:
            if mp.token == token:
                mp.nombre = nuevo_nombre
                return
        raise ValueError("Método de pago no encontrado.")

    def eliminar_metodo_pago(self, token: str):
        for mp in self.metodos_pago:
            if mp.token == token:
                self.metodos_pago.remove(mp)
                return
        raise ValueError("Método de pago no encontrado.")

@dataclass(kw_only=True)
class ClienteEmpresa(Usuario):
    rut: Rut
    fecha_constitucion: datetime = field(default_factory=datetime)
