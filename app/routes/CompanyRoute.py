#!/usr/bin/env python
import flask
from flask import request, jsonify, g
from app import db
from sqlalchemy import and_
from flask_httpauth import HTTPBasicAuth

from werkzeug.security import generate_password_hash, check_password_hash
from app.routes import api
from app.models.Company import Company
from app.routes.validations.CompanyCreateInputSchema import CompanyCreateInputSchema

from datetime import datetime

auth = HTTPBasicAuth()

create_company_schema = CompanyCreateInputSchema()
@api.route('/api/companies', methods=['POST'])
def new_company():
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
    company = Company(name=name,
                phone_number=phone_number, 
                phone_region=phone_region, 
                status=1, # ATIVO
                created_at=datetime.now(),
                updated_at=datetime.now())

    if company.query.filter(and_(Company.phone_region==phone_region,Company.phone_number==phone_number)).first() is not None:
        return (jsonify({'message': 'Company already exists'}), 400)

    # user.hash_password(req_data['password'])
    db.session.add(company)
    db.session.commit()

    response = flask.make_response(jsonify({ 'data': {
                                        'id': company.id,
                                        'name': company.name, 
                                        'phone_region': company.phone_region,
                                        'phone_number': company.phone_number,
                                        'status': company.status}}), 201)
    response.headers["Content-Type"] = "application/json"
    return response


@api.route('/api/companies/<int:id>', methods=['GET'])
def get_company(id):
    company = Company.query.get(id)
    if not company:
        return (jsonify({'message': 'Company not found'}), 404)
    
    response = flask.make_response(jsonify({ 'data': {
                                        'id': company.id,
                                        'name': company.name, 
                                        'phone_region': company.phone_region,
                                        'phone_number': company.phone_number,
                                        'status': company.status}}), 200)
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

@api.route('/api/companies/currentuser')
def get_current_company():
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