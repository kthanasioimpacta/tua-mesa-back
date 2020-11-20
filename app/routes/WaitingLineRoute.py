#!/usr/bin/env python

from flask import request, jsonify, g
from flask_httpauth import HTTPBasicAuth

from app.routes import api

from app.routes.validations.WaitingLineCreateInputSchema import WaitingLineCreateInputSchema
from app.shared.HandleRequestValidation import handle_request_validation
from app.routes.validations.errors.ValidationError import ValidationError

from app.shared.Authentication import is_logged, is_admin

from app.services import WaitingLineService

auth = HTTPBasicAuth()

@api.route('/api/waiting-lines', methods=['POST'])
def new_waiting_line():
    req_data = request.get_json()
    data_schema = WaitingLineCreateInputSchema()
    try:
        handle_request_validation(data_schema)
    except ValidationError as err:
        return jsonify(err.message), 400

    if not is_logged() or not is_admin():
        return (jsonify({'message': 'Not Authorized' })), 401
        
    return WaitingLineService.save(req_data)


@api.route('/api/waiting-lines', methods=['GET'])
def get_waiting_lines():
    if not is_logged():
        return (jsonify({'message': 'Not Authorized' })), 401

    return WaitingLineService.getAll()

@api.route('/api/waiting-lines/<int:id>', methods=['GET'])
def get_waiting_line(id):
    if not is_logged():
        return (jsonify({'message': 'Not Authorized' })), 401

    return WaitingLineService.get(id)


@api.route('/api/waiting-lines/position', methods=['GET'])
def get_position():
    return WaitingLineService.getPosition(request.args['token'])
