import sqlite3
from aeroalpes.modulos.cliente.dominio.entidades import ClienteNatural as Cliente
from aeroalpes.modulos.cliente.dominio.objetos_valor import MetodoPago, TipoMetodoPago, Email, Cedula
from aeroalpes.modulos.cliente.dominio.repositorios import RepositorioCliente

class RepositorioClienteSQLite(RepositorioCliente):
    def __init__(self, db_path='aeroalpes_clientes.db'):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._crear_tablas()

    def _crear_tablas(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id TEXT PRIMARY KEY,
                nombre TEXT,
                apellido TEXT,
                email TEXT,
                cedula TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS metodos_pago (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id TEXT,
                tipo TEXT,
                nombre TEXT,
                token TEXT,
                FOREIGN KEY(cliente_id) REFERENCES clientes(id)
            )
        ''')
        self.conn.commit()

    def agregar(self, cliente: Cliente):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO clientes (id, nombre, apellido, email, cedula)
            VALUES (?, ?, ?, ?, ?)
        ''', (cliente.id, cliente.nombre, cliente.apellido, cliente.email.direccion, cliente.cedula.numero))
        for mp in cliente.metodos_pago:
            cursor.execute('''
                INSERT INTO metodos_pago (cliente_id, tipo, nombre, token)
                VALUES (?, ?, ?, ?)
            ''', (cliente.id, mp.tipo.value, mp.nombre, mp.token))
        self.conn.commit()

    def actualizar(self, cliente: Cliente):
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE clientes
            SET nombre = ?, apellido = ?, email = ?, cedula = ?
            WHERE id = ?
        ''', (cliente.nombre, cliente.apellido, cliente.email.direccion, cliente.cedula.numero, cliente.id))
        # Se actualizan los métodos de pago de forma simplificada: se eliminan y se reinsertan.
        cursor.execute('DELETE FROM metodos_pago WHERE cliente_id = ?', (cliente.id,))
        for mp in cliente.metodos_pago:
            cursor.execute('''
                INSERT INTO metodos_pago (cliente_id, tipo, nombre, token)
                VALUES (?, ?, ?, ?)
            ''', (cliente.id, mp.tipo.value, mp.nombre, mp.token))
        self.conn.commit()

    def eliminar(self, cliente: Cliente):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM metodos_pago WHERE cliente_id = ?', (cliente.id,))
        cursor.execute('DELETE FROM clientes WHERE id = ?', (cliente.id,))
        self.conn.commit()

    def obtener_por_id(self, id: str) -> Cliente:
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM clientes WHERE id = ?', (id,))
        row = cursor.fetchone()
        if row:
            cliente = Cliente(row['nombre'], row['apellido'], Email(row['email']), Cedula(row['cedula']))
            cliente.id = row['id']
            cursor.execute('SELECT * FROM metodos_pago WHERE cliente_id = ?', (id,))
            for mp_row in cursor.fetchall():
                mp = MetodoPago(TipoMetodoPago(mp_row['tipo']), mp_row['nombre'], mp_row['token'])
                cliente.metodos_pago.append(mp)
            return cliente
        else:
            return None
