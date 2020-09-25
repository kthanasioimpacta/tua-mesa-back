#!/usr/bin/env python
import flask
from flask import request, jsonify, g, current_app
from app import db
from sqlalchemy import or_, and_
from flask_httpauth import HTTPBasicAuth

from werkzeug.security import generate_password_hash, check_password_hash
from app.routes import api
from app.models.User import User
from app.routes.validations.UserCreateInputSchema import UserCreateInputSchema

import time
from datetime import datetime
from app.shared.Util import format_datetime
from app.shared.Authentication import is_logged

from app.shared.HandleRequestValidation import handle_request_validation
from app.routes.validations.errors.ValidationError import ValidationError

auth = HTTPBasicAuth()

@api.route('/api/users', methods=['POST'])
def new_user():
    req_data = request.get_json()
    data_schema = UserCreateInputSchema()
    try:
        handle_request_validation(data_schema)
    except ValidationError as err:
        return jsonify(err.message), 400

    username = req_data['username']
    email = req_data['email']
    if 'phone_region' not in req_data:
        phone_region = '+55'
    else:
        phone_region = req_data['phone_region']
    user = User(username=username, 
                email=email, 
                company_id=req_data['company_id'], 
                phone_number=req_data['phone_number'], 
                phone_region=phone_region, 
                role_id=req_data['role_id'], 
                status=1, # ATIVO
                created_at=datetime.now(),
                updated_at=datetime.now())

    if User.query.filter(or_(User.email==email,User.username==username)).first() is not None:
        return (jsonify({'message': 'User already exists'}), 400)

    user.hash_password(req_data['password'])
    db.session.add(user)
    db.session.commit()

    response = flask.make_response(jsonify({ 'data': {
                                        'id': user.id,
                                        'username': user.username, 
                                        'company_id': user.company_id,
                                        'email': user.email,
                                        'phone_region': user.phone_region,
                                        'phone_number': user.phone_number,
                                        'status': user.status,
                                        'role_id': user.role_id,
                                        'created_at': format_datetime(user.created_at),
                                        'updated_at': format_datetime(user.updated_at)}}), 201)
    response.headers["Content-Type"] = "application/json"
    return response


@api.route('/api/users/<int:id>', methods=['GET'])
def get_user(id):
    if not is_logged():
        return (jsonify({'message': 'Not Authorized' })), 401
    user = User.query.filter(and_(User.id==id,User.company_id==g.user.company_id)).first()
    if not user:
        return (jsonify({'message': 'User not found'}), 404)
    
    response = flask.make_response(jsonify({ 'data': {
                                        'id': user.id,
                                        'username': user.username, 
                                        'company_id': user.company_id,
                                        'email': user.email,
                                        'phone_region': user.phone_region,
                                        'phone_number': user.phone_number,
                                        'status': user.status,
                                        'role_id': user.role_id,
                                        'created_at': format_datetime(user.created_at),
                                        'updated_at': format_datetime(user.updated_at)}}), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@api.route('/health')
def get_health():
    response = flask.make_response({'message': 'ok'}, 200)
    response.headers["Content-Type"] = "application/json"
    return response

@api.route('/api/users/login', methods=['POST'])
@auth.login_required
def get_auth_token():
    req_data = request.get_json()
    
    if req_data['email'] != g.user.email:
        return (jsonify({'message': 'Not Authorized' })), 401

    token = g.user.generate_auth_token(current_app.config['TOKEN_TTL'])

    response = flask.make_response({'token': token.decode('ascii'), 'duration': current_app.config['TOKEN_TTL']}, 200)
    response.headers["Content-Type"] = "application/json"
    
    lease = 14 * 24 * 60 * 60  # 14 days in seconds
    end = time.gmtime(time.time() + lease)
    expires = time.strftime("%a, %d-%b-%Y %T GMT", end)

    response.set_cookie('token', token.decode('ascii'), secure=False, domain='.tuamesa.com.br', expires=expires)
    return response

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

@api.route('/api/users/currentuser')
def get_current_user():
    if not is_logged():
        return (jsonify({'message': 'Not Authorized' })), 401
    response = flask.make_response({ 'data': {
                                        'id': g.user.id,
                                        'username': g.user.username, 
                                        'company_id': g.user.company_id,
                                        'email': g.user.email,
                                        'phone_region': g.user.phone_region,
                                        'phone_number': g.user.phone_number,
                                        'status': g.user.status,
                                        'role_id': g.user.role_id,
                                        'created_at': format_datetime(g.user.created_at),
                                        'updated_at': format_datetime(g.user.updated_at)}}, 200)
    return response
