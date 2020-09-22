#!/usr/bin/env python

import flask
from flask import request, jsonify, g
from app import db
from sqlalchemy import and_
from flask_httpauth import HTTPBasicAuth

# from werkzeug.security import generate_password_hash, check_password_hash
from app.routes import api
from app.models.Company import Company
from app.routes.validations.CompanyCreateInputSchema import CompanyCreateInputSchema

from datetime import datetime
from app.shared.Util import format_datetime
from app.shared.HandleRequestValidation import handle_request_validation
from app.shared.Authentication import is_logged, is_admin

from app.routes.validations.errors.ValidationError import ValidationError

auth = HTTPBasicAuth()

@api.route('/api/companies', methods=['POST'])
def new_company():
    req_data = request.get_json()
    data_schema = CompanyCreateInputSchema()
    try:
        handle_request_validation(data_schema)
    except ValidationError as err:
        return jsonify(err.message), 400
    
    name = req_data['name']
    if 'phone_region' not in req_data:
        phone_region = '+55'
    else:
        phone_region = req_data['phone_region']
    phone_number=req_data['phone_number']
    company = Company(  name=name,
                        phone_number=phone_number, 
                        phone_region=phone_region, 
                        status=1, # ATIVO
                        created_at=datetime.now(),
                        updated_at=datetime.now())

    if company.query.filter(and_(Company.phone_region==phone_region,Company.phone_number==phone_number)).first() is not None:
        return (jsonify({'message': 'Company already exists'}), 400)

    db.session.add(company)
    db.session.commit()

    response = flask.make_response(jsonify({ 'data': {
                                        'id': company.id,
                                        'name': company.name, 
                                        'phone_region': company.phone_region,
                                        'phone_number': company.phone_number,
                                        'status': company.status,
                                        'created_at': format_datetime(company.created_at),
                                        'updated_at': format_datetime(company.updated_at)}}), 201)
    response.headers["Content-Type"] = "application/json"
    return response


@api.route('/api/companies/<int:id>', methods=['GET'])
def get_company(id):
    if not is_logged() or id != g.user.company_id or not is_admin():
        return (jsonify({'message': 'Not Authorized' })), 401
    
    company = Company.query.get(id)
    if not company:
        return (jsonify({'message': 'Company not found'}), 404)
    
    response = flask.make_response(jsonify({ 'data': {
                                        'id': company.id,
                                        'name': company.name, 
                                        'phone_region': company.phone_region,
                                        'phone_number': company.phone_number,
                                        'status': company.status,
                                        'created_at': format_datetime(company.created_at),
                                        'updated_at': format_datetime(company.updated_at)}}), 200)
    response.headers["Content-Type"] = "application/json"
    return response
