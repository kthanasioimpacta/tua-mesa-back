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
from app.shared.Util import format_datetime

from app.shared.Authentication import is_logged, is_admin
from app.shared.HandleRequestValidation import handle_request_validation
from app.routes.validations.errors.ValidationError import ValidationError

auth = HTTPBasicAuth()

@api.route('/api/waiting-lines', methods=['POST'])
def new_waiting_line():
    req_data = request.get_json()
    data_schema = WaitingLineCreateInputSchema()
    try:
        handle_request_validation(data_schema)
    except ValidationError as err:
        return jsonify(err.message), 400

    if not is_logged() or req_data['company_id'] != g.user.company_id or not is_admin():
        return (jsonify({'message': 'Not Authorized' })), 401
        
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
                                        'status': waiting_line.status,
                                        'created_at': format_datetime(waiting_line.created_at),
                                        'updated_at': format_datetime(waiting_line.updated_at)}}), 201)
    response.headers["Content-Type"] = "application/json"
    return response


@api.route('/api/waiting-lines', methods=['GET'])
def get_waiting_lines():
    if not is_logged():
        return (jsonify({'message': 'Not Authorized' })), 401

    waiting_lines = WaitingLine.query.filter_by(company_id=g.user.company_id).all()
    if not waiting_lines:
        return (jsonify({'message': 'No Waiting Lines found'}), 404)
    resp = {'data': []} 
    for waiting_line in waiting_lines:
        resp['data'].append( {  'id': waiting_line.id,
                                'company_id': waiting_line.company_id,
                                'name': waiting_line.name, 
                                'is_priority': waiting_line.is_priority,
                                'status': waiting_line.status,
                                'created_at': format_datetime(waiting_line.created_at),
                                'updated_at': format_datetime(waiting_line.updated_at)})
    response = flask.make_response(jsonify(resp), 200)
    
    response.headers["Content-Type"] = "application/json"
    return response

@api.route('/api/waiting-lines/<int:id>', methods=['GET'])
def get_waiting_line(id):

    waiting_line = WaitingLine.query.get(id)
    if not waiting_line:
        return (jsonify({'message': 'Waiting Line not found'}), 404)
    
    if not is_logged() or waiting_line.company_id != g.user.company_id:
        return (jsonify({'message': 'Not Authorized' })), 401


    response = flask.make_response(jsonify({ 'data': {
                                        'id': waiting_line.id,
                                        'company_id': waiting_line.company_id,
                                        'name': waiting_line.name, 
                                        'is_priority': waiting_line.is_priority,
                                        'status': waiting_line.status,
                                        'created_at': format_datetime(waiting_line.created_at),
                                        'updated_at': format_datetime(waiting_line.updated_at)}}), 200)
    response.headers["Content-Type"] = "application/json"
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
