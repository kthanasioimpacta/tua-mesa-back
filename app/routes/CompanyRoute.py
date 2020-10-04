#!/usr/bin/env python

import flask
from flask import request, jsonify, g
from flask_httpauth import HTTPBasicAuth

from app.routes import api
from app.routes.validations.CompanyCreateInputSchema import CompanyCreateInputSchema

from app.shared.HandleRequestValidation import handle_request_validation
from app.shared.Authentication import is_logged, is_admin

from app.routes.validations.errors.ValidationError import ValidationError

from app.services import CompanyService

auth = HTTPBasicAuth()

@api.route('/api/companies', methods=['POST'])
def new_company():
    req_data = request.get_json()
    data_schema = CompanyCreateInputSchema()
    try:
        handle_request_validation(data_schema)
    except ValidationError as err:
        return jsonify(err.message), 400
    
    return CompanyService.save(req_data)


@api.route('/api/companies/<int:id>', methods=['GET'])
def get_company(id):
    if not is_logged() or id != g.user.company_id or not is_admin():
        return (jsonify({'message': 'Not Authorized' })), 401
    
    return CompanyService.get(id)
