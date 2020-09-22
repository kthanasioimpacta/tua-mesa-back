#!/usr/bin/env python
import flask
from flask import request, jsonify, g
from app import db
from sqlalchemy import and_
from flask_httpauth import HTTPBasicAuth

from werkzeug.security import generate_password_hash, check_password_hash
from app.routes import api
from app.models.Customer import Customer
from app.routes.validations.CustomerCreateInputSchema import CustomerCreateInputSchema

from datetime import datetime
from app.shared.Util import format_datetime
from app.shared.HandleRequestValidation import handle_request_validation
from app.shared.Authentication import is_logged, is_admin

from app.routes.validations.errors.ValidationError import ValidationError

auth = HTTPBasicAuth()

@api.route('/api/customers', methods=['POST'])
def new_customer():
    req_data = request.get_json()
    data_schema = CustomerCreateInputSchema()
    try:
        handle_request_validation(data_schema)
    except ValidationError as err:
        return jsonify(err.message), 400

    if not is_logged():
        return (jsonify({'message': 'Not Authorized' })), 401

    name = req_data['name']
    if 'phone_region' not in req_data:
        phone_region = '+55'
    else:
        phone_region = req_data['phone_region']
    phone_number=req_data['phone_number']
    description = None
    if 'description' in req_data:
        description = req_data['description']
    email = None
    if 'email' in req_data:
        email = req_data['email']
    customer = Customer(name=name,
                phone_number=phone_number, 
                phone_region=phone_region, 
                description=description,
                email=email,
                status=1, # ATIVO
                created_at=datetime.now(),
                updated_at=datetime.now())

    if customer.query.filter(and_(Customer.phone_region==phone_region,Customer.phone_number==phone_number)).first() is not None:
        return (jsonify({'message': 'Customer already exists'}), 400)

    # user.hash_password(req_data['password'])
    db.session.add(customer)
    db.session.commit()

    response = flask.make_response(jsonify({ 'data': {
                                        'id': customer.id,
                                        'name': customer.name, 
                                        'phone_region': customer.phone_region,
                                        'phone_number': customer.phone_number,
                                        'description': description,
                                        'email': email,
                                        'status': customer.status,
                                        'created_at': format_datetime(customer.created_at),
                                        'updated_at': format_datetime(customer.updated_at)}}), 201)
    response.headers["Content-Type"] = "application/json"
    return response


@api.route('/api/customers/<int:id>', methods=['GET'])
def get_customer(id):

    if not is_logged():
        return (jsonify({'message': 'Not Authorized' })), 401

    customer = Customer.query.get(id)
    if not customer:
        return (jsonify({'message': 'Customer not found'}), 404)
    
    response = flask.make_response(jsonify({ 'data': {
                                        'id': customer.id,
                                        'name': customer.name, 
                                        'phone_region': customer.phone_region,
                                        'phone_number': customer.phone_number,
                                        'description': customer.description,
                                        'email': customer.email,
                                        'status': customer.status,
                                        'created_at': format_datetime(customer.created_at),
                                        'updated_at': format_datetime(customer.updated_at)}}), 200)
    response.headers["Content-Type"] = "application/json"
    return response

