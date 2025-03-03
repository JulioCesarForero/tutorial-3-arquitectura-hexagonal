import aeroalpes.seedwork.presentacion.api as api
import json
from flask import redirect, render_template, request, session, url_for
from flask import Response

from aeroalpes.modulos.cliente.aplicacion.servicios import ServicioCliente
from aeroalpes.modulos.cliente.aplicacion.mapeadores import MapeadorClienteDTOJson, MapeadorMetodoPagoDTOJson
from aeroalpes.seedwork.dominio.excepciones import ExcepcionDominio

bp = api.crear_blueprint('cliente', '/clientes')

@bp.route('/cliente', methods=['POST'])
def registrar_cliente():
    try:
        data = request.json

        mapper = MapeadorClienteDTOJson()
        cliente_dto = mapper.externo_a_dto(data)

        servicio = ServicioCliente()
        resultado = servicio.registrar_usuario(cliente_dto)

        return Response(json.dumps(mapper.dto_a_externo(resultado)), status=201, mimetype='application/json')
    except Exception as e:
        return Response(json.dumps({"error": str(e)}), status=400, mimetype='application/json')

@bp.route('/cliente/<cliente_id>/metodos', methods=['POST'])
def agregar_metodo_pago(cliente_id):
    try:
        data = request.json
        mapper = MapeadorMetodoPagoDTOJson()
        metodo_dto = mapper.externo_a_dto(data)
        servicio = ServicioCliente()
        resultado = servicio.agregar_metodo_pago(cliente_id, metodo_dto)
        return Response(json.dumps(resultado), status=201, mimetype='application/json')
    except Exception as e:
        return Response(json.dumps({"error": str(e)}), status=400, mimetype='application/json')

@bp.route('/cliente/<cliente_id>/metodos', methods=['PUT'])
def modificar_metodo_pago(cliente_id):
    try:
        data = request.json
        mapper = MapeadorMetodoPagoDTOJson()
        metodo_dto = mapper.externo_a_dto(data)
        servicio = ServicioCliente()
        resultado = servicio.modificar_metodo_pago(cliente_id, metodo_dto)
        return Response(json.dumps(resultado), status=200, mimetype='application/json')
    except Exception as e:
        return Response(json.dumps({"error": str(e)}), status=400, mimetype='application/json')

@bp.route('/cliente/<cliente_id>/metodos/<token>', methods=['DELETE'])
def eliminar_metodo_pago(cliente_id, token):
    try:
        servicio = ServicioCliente()
        resultado = servicio.eliminar_metodo_pago(cliente_id, token)
        return Response(json.dumps(resultado), status=200, mimetype='application/json')
    except Exception as e:
        return Response(json.dumps({"error": str(e)}), status=400, mimetype='application/json')
