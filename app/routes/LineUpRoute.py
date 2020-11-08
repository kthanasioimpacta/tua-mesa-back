#!/usr/bin/env python
import flask
from flask import request, jsonify
from flask_httpauth import HTTPBasicAuth

from app.routes import api

from app.routes.validations.LineUpCreateInputSchema import LineUpCreateInputSchema
from app.shared.HandleRequestValidation import handle_request_validation
from app.routes.validations.errors.ValidationError import ValidationError

from app.shared.Authentication import is_logged

from app.services import LineUpService

auth = HTTPBasicAuth()

@api.route('/api/line-ups', methods=['POST'])
def new_line_up():
    data_schema = LineUpCreateInputSchema()
    try:
        handle_request_validation(data_schema)
    except ValidationError as err:
        return jsonify(err.message), 400

    return LineUpService.save(request.get_json())

@api.route('/api/line-ups/<int:id>', methods=['GET'])
def list_line_up(id):
    return LineUpService.getAll(id)


@api.route('/api/line-ups/next-customer', methods=['GET'])
def get_next_customer():

    if not is_logged(): # TODO: VALIDAR SE O USUÁRIO PERTENCE A EMPRESA
        return (jsonify({'message': 'Not Authorized' })), 401
    waiting_line_id = request.args['waiting_line_id']
    return LineUpService.get_next_customer(waiting_line_id)

@api.route('/api/line-ups/<int:id>/call-customer', methods=['PUT'])
def call_customer(id):

    if not is_logged(): # TODO: VALIDAR SE O USUÁRIO PERTENCE A EMPRESA
        return (jsonify({'message': 'Not Authorized' })), 401
    return LineUpService.call_customer(id)
