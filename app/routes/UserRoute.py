#!/usr/bin/env python
import flask
from app.routes import api

from app.routes.validations.errors.ValidationError import ValidationError
from app.routes.validations.UserCreateInputSchema import UserCreateInputSchema
from app.shared.HandleRequestValidation import handle_request_validation

from app.shared.Authentication import is_logged
from flask import current_app, g, request, jsonify
from flask_httpauth import HTTPBasicAuth

from app.services import UserService

auth = HTTPBasicAuth()

@api.route('/api/users', methods=['POST'])
def new_user():
    data_schema = UserCreateInputSchema()
    try:
        handle_request_validation(data_schema)
    except ValidationError as err:
        return jsonify(err.message), 400
    return UserService.save(request.get_json())

@api.route('/api/users/<int:id>', methods=['GET'])
def get_user(id):
    if not is_logged():
        return (jsonify({'message': 'Not Authorized' })), 401
    return UserService.get(id)

@api.route('/health')
def get_health():
    response = flask.make_response({'message': 'ok'}, 200)
    response.headers["Content-Type"] = "application/json"
    return response

@api.route('/api/users/login', methods=['POST'])
@auth.login_required
def get_auth_token():
  return UserService.get_auth_token(request.get_json())
    
@auth.verify_password
def verify_password(pid, password='password'):
    return UserService.verify_password(pid, password)

@api.route('/api/users/currentuser')
def get_current_user():
    if not is_logged():
        return (jsonify({'message': 'Not Authorized' })), 401
    return UserService.get_current_user()
