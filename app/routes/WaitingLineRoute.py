#!/usr/bin/env python
import flask
from flask import request, jsonify, g
from app import db
from sqlalchemy import and_
from flask_httpauth import HTTPBasicAuth

from werkzeug.security import generate_password_hash, check_password_hash
from app.routes import api
from app.models.WaitingLine import WaitingLine
from app.routes.validations.WaitingLineCreateInputSchema import WaitingLineCreateInputSchema

from datetime import datetime

auth = HTTPBasicAuth()

create_waiting_line_schema = WaitingLineCreateInputSchema()
@api.route('/api/waiting-lines', methods=['POST'])
def new_waiting_line():
    req_data = request.get_json()
    errors = create_waiting_line_schema.validate(req_data)
    error_list = []
    for k, v in errors.items():
        error_list.append({k: v})
    if errors:
        return (jsonify({'errors': error_list}), 400)
    name = req_data['name']
    waiting_line = WaitingLine(name=name,
                company_id=req_data['company_id'],
                status=1, # ATIVO
                is_priority=req_data['is_priority'],
                created_at=datetime.now(),
                updated_at=datetime.now())

    if waiting_line.query.filter(and_(WaitingLine.company_id==req_data['company_id'],WaitingLine.name==name)).first() is not None:
        return (jsonify({'message': 'Company already exists'}), 400)

    # user.hash_password(req_data['password'])
    db.session.add(waiting_line)
    db.session.commit()

    response = flask.make_response(jsonify({ 'data': {
                                        'id': waiting_line.id,
                                        'company_id': waiting_line.company_id,
                                        'name': waiting_line.name, 
                                        'is_priority': waiting_line.is_priority,
                                        'status': waiting_line.status}}), 201)
    response.headers["Content-Type"] = "application/json"
    return response


@api.route('/api/waiting-lines/<int:id>', methods=['GET'])
def get_waiting_line(id):
    waiting_line = WaitingLine.query.get(id)
    if not waiting_line:
        return (jsonify({'message': 'Waiting Line not found'}), 404)
    
    response = flask.make_response(jsonify({ 'data': {
                                        'id': waiting_line.id,
                                        'company_id': waiting_line.company_id,
                                        'name': waiting_line.name, 
                                        'is_priority': waiting_line.is_priority,
                                        'status': waiting_line.status}}), 200)
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
def get_current_waiting_line():
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