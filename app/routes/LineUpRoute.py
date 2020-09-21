#!/usr/bin/env python
import flask
from flask import request, jsonify, g
from app import db
from sqlalchemy import and_
from flask_httpauth import HTTPBasicAuth

from werkzeug.security import generate_password_hash, check_password_hash
from app.routes import api
from app.models.LineUp import LineUp
from app.routes.validations.LineUpCreateInputSchema import LineUpCreateInputSchema

from datetime import datetime
from app.shared.Util import format_datetime

from app.shared.Authentication import is_logged, is_admin

auth = HTTPBasicAuth()

create_line_up_schema = LineUpCreateInputSchema()
@api.route('/api/line-ups', methods=['POST'])
def new_line_up():
    req_data = request.get_json()
    errors = create_line_up_schema.validate(req_data)
    error_list = []
    for k, v in errors.items():
        error_list.append({k: v})
    if errors:
        return (jsonify({'errors': error_list}), 400)

    line_up = LineUp(waiting_line_id= req_data['waiting_line_id'],
                     customer_id= req_data['customer_id'],
                     status=0, # ENTROU NA FILA
                     joined_at=datetime.now())

    if line_up.query.filter(and_(LineUp.customer_id==req_data['customer_id'],LineUp.status < 3)).first() is not None:
        return (jsonify({'message': 'Customer already in an active Waiting Line'}), 400)

    if not is_logged(): # TODO: VALIDAR SE O USUÁRIO PERTENCE A EMPRESA
        return (jsonify({'message': 'Not Authorized' })), 401

    db.session.add(line_up)
    db.session.commit()

    response = flask.make_response(jsonify({ 'data': {
                                        'id': line_up.id,
                                        'customer_id': line_up.customer_id,
                                        'waiting_line_id': line_up.waiting_line_id,
                                        'status': line_up.status,
                                        'joined_at': format_datetime(line_up.joined_at)}}), 201)
    response.headers["Content-Type"] = "application/json"
    return response


@api.route('/api/line-ups/next-customer', methods=['GET'])
def get_next_customer():
    waiting_line_id = request.args['waiting_line_id']
    line_up = LineUp()
    next_customer = line_up.query.filter(and_(LineUp.waiting_line_id==waiting_line_id,LineUp.status == 0)).order_by(db.asc('joined_at')).first()
    if not next_customer:
        return (jsonify({'message': 'Fila de espera vazia'}), 404)

    response = flask.make_response(jsonify({ 'data': {
                                        'id': next_customer.id,
                                        'customer_id': next_customer.customer_id,
                                        'waiting_line_id': next_customer.waiting_line_id,
                                        'status': next_customer.status,
                                        'joined_at': format_datetime(next_customer.joined_at) }}), 200)
    response.headers["Content-Type"] = "application/json"
    return response

@api.route('/api/line-ups/<int:id>/call-customer', methods=['PUT'])
def call_customer(id):
    line_up = LineUp.query.get(id)
    if not line_up:
        return (jsonify({'message': 'Record not found'}), 404)
    
    if line_up.first_call_at is None:
        line_up.first_call_at = datetime.now()
        line_up.status = 1 # first_call
    else:
        if line_up.second_call_at is None:
            line_up.second_call_at = datetime.now()
            line_up.status = 2 # second call
        else:
            line_up.cancelled_call_at = datetime.now()
            line_up.status = 4 # cancelled
            db.session.add(line_up)
            db.session.commit()
            return (jsonify({'message': 'Atendimento Cancelado! Cliente não atendeu a segunda chamada!'}), 400)

    db.session.add(line_up)
    db.session.commit()

    response = flask.make_response(jsonify({ 'data': {
                                        'id': line_up.id,
                                        'customer_id': line_up.customer_id,
                                        'waiting_line_id': line_up.waiting_line_id,
                                        'joined_at': format_datetime(line_up.joined_at),
                                        'first_call_at': format_datetime(line_up.first_call_at),
                                        'second_call_at': format_datetime(line_up.second_call_at),
                                        'completed_call_at': format_datetime(line_up.completed_call_at),
                                        'cancelled_call_at': format_datetime(line_up.cancelled_call_at),
                                        'status': line_up.status}}), 200)
    response.headers["Content-Type"] = "application/json"
    return response
