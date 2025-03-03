"""Objetos valor del dominio de cliente

En este archivo usted encontrará los objetos valor del dominio de cliente

"""

from aeroalpes.seedwork.dominio.objetos_valor import ObjetoValor, Ciudad
from dataclasses import dataclass
from enum import Enum
import re



@dataclass(frozen=True)
class Nombre(ObjetoValor):
    nombres: str
    apellidos: str

@dataclass(frozen=True)
class Email(ObjetoValor):
    address: str
    dominio: str
    es_empresarial: bool

@dataclass(frozen=True)
class Cedula(ObjetoValor):
    numero: int
    ciudad: Ciudad

@dataclass(frozen=True)
class Rut(ObjetoValor):
    numero: int
    ciudad: Ciudad

class TipoMetodoPago(Enum):
    TARJETA_CREDITO = "tarjeta_credito"
    TARJETA_DEBITO = "tarjeta_debito"
    TRANSFERENCIA_BANCARIA = "transferencia_bancaria"
    OTRO = "otro"


@dataclass(frozen=True)
class MetodoPago:
    def __init__(self, tipo: TipoMetodoPago, nombre: str, token: str):
        self.validar_nombre(nombre)
        self.tipo = tipo
        self.nombre = nombre
        self.token = token  # Token único generado externamente o aquí mismo

    @staticmethod
    def validar_nombre(nombre: str):
        if not (5 <= len(nombre) <= 80):
            raise ValueError("El nombre del método de pago debe tener entre 5 y 80 caracteres.")
        # Permitir solo letras, números y espacios
        if not re.match(r'^[A-Za-z0-9\s]+$', nombre):
            raise ValueError("El nombre del método de pago no puede contener caracteres especiales.")

class Email:
    def __init__(self, address: str):
        if not address:
            raise ValueError("La dirección de correo electrónico es obligatoria.")
        self.validar(address)
        self.address = address

    @staticmethod
    def validar(address: str):
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', address):
            raise ValueError("El correo electrónico no es válido.")


class Cedula:
    def __init__(self, numero: str):
        self.validar(numero)
        self.numero = numero

    @staticmethod
    def validar(numero: str):
        if not numero.isdigit():
            raise ValueError("La cédula debe contener solo números.")


