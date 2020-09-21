#!/usr/bin/env python
import flask
from flask import request, jsonify, g
from app import db
from sqlalchemy import or_
from flask_httpauth import HTTPBasicAuth

from werkzeug.security import generate_password_hash, check_password_hash
from app.routes import api
from app.models.User import User
from app.routes.validations.UserCreateInputSchema import UserCreateInputSchema

from datetime import datetime

auth = HTTPBasicAuth()

create_user_schema = UserCreateInputSchema()
@api.route('/api/users', methods=['POST'])
def new_user():
    req_data = request.get_json()
    errors = create_user_schema.validate(req_data)
    error_list = []
    for k, v in errors.items():
        error_list.append({k: v})
    if errors:
        return (jsonify({'errors': error_list}), 400)

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
                                        'email': user.email,
                                        'phone_region': user.phone_region,
                                        'phone_number': user.phone_number,
                                        'status': user.status}}), 201)
    response.headers["Content-Type"] = "application/json"
    return response


@api.route('/api/users/<int:id>', methods=['GET'])
def get_user(id):
    if not is_logged():
        return (jsonify({'message': 'Not Authorized' })), 401
    user = User.query.get(id)
    if not user:
        return (jsonify({'message': 'User not found'}), 404)
    
    response = flask.make_response(jsonify({ 'data': {
                                        'id': user.id,
                                        'username': user.username, 
                                        'email': user.email,
                                        'phone_region': user.phone_region,
                                        'phone_number': user.phone_number,
                                        'status': user.status}}), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@api.route('/api/users/login')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(600)

    response = flask.make_response({'token': token.decode('ascii'), 'duration': 600}, 200)
    response.headers["Content-Type"] = "application/json"
    response.set_cookie('token', token.decode('ascii'), secure=False)
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
def get_resource():
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