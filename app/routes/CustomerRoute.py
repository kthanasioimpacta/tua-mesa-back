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

auth = HTTPBasicAuth()

create_company_schema = CustomerCreateInputSchema()
@api.route('/api/customers', methods=['POST'])
def new_customer():
    req_data = request.get_json()
    errors = create_company_schema.validate(req_data)
    error_list = []
    for k, v in errors.items():
        error_list.append({k: v})
    if errors:
        return (jsonify({'errors': error_list}), 400)
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
                                        'status': customer.status}}), 201)
    response.headers["Content-Type"] = "application/json"
    return response


@api.route('/api/customers/<int:id>', methods=['GET'])
def get_customer(id):
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
                                        'status': customer.status}}), 200)
    response.headers["Content-Type"] = "application/json"
    return response


# @api.route('/api/companies/login')
# @auth.login_required
# def get_auth_token():
#     token = g.user.generate_auth_token(600)

#     response = flask.make_response({'token': token.decode('ascii'), 'duration': 600}, 200)
#     response.headers["Content-Type"] = "application/json"
#     response.set_cookie('token', token.decode('ascii'), secure=False)
#     return response

@auth.verify_password
def verify_password(pid, password='password'):
    # first try to authenticate by token
    user = User.verify_auth_token(pid)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=pid).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True

@api.route('/api/customers/currentuser')
def get_current_customer():
    if not is_logged():
        return (jsonify({'message': 'Not Authorized' })), 401
    response = flask.make_response({ 'data': {
                                        'id': g.user.id,
                                        'username': g.user.username, 
                                        'email': g.user.email,
                                        'phone_region': g.user.phone_region,
                                        'phone_number': g.user.phone_number,
                                        'status': g.user.status}}, 200)
    return response

def is_logged():
    return verify_password(request.cookies.get('token'))