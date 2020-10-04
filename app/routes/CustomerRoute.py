#!/usr/bin/env python
import flask
from flask import request, jsonify, g
from flask_httpauth import HTTPBasicAuth

from app.routes import api

from app.routes.validations.CustomerCreateInputSchema import CustomerCreateInputSchema
from app.routes.validations.errors.ValidationError import ValidationError
from app.shared.HandleRequestValidation import handle_request_validation

from app.shared.Authentication import is_logged

from app.services import CustomerService

auth = HTTPBasicAuth()

@api.route('/api/customers', methods=['POST'])
def new_customer():
    data_schema = CustomerCreateInputSchema()
    try:
        handle_request_validation(data_schema)
    except ValidationError as err:
        return jsonify(err.message), 400
    if not is_logged():
        return (jsonify({'message': 'Not Authorized' })), 401
    return CustomerService.save(request.get_json())


@api.route('/api/customers/<int:id>', methods=['GET'])
def get_customer(id):
    if not is_logged():
        return (jsonify({'message': 'Not Authorized' })), 401
    return CustomerService.get(id)

