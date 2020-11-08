import flask
from flask import jsonify, request
from app import db
from sqlalchemy import and_
from datetime import datetime
from app.shared.Util import format_datetime

from app.shared.Authentication import is_logged, is_admin

from app.models.LineUp import LineUp

def save(data):
  line_up = LineUp(waiting_line_id= data['waiting_line_id'],
                     customer_id= data['customer_id'],
                     status=0, # ENTROU NA FILA
                     joined_at=datetime.now())

  if not is_logged(): # TODO: VALIDAR SE O USUÁRIO PERTENCE A EMPRESA
      return (jsonify({'message': 'Not Authorized' })), 401

  if line_up.query.filter(and_(LineUp.customer_id==data['customer_id'],LineUp.status < 3)).first() is not None:
      return (jsonify({'message': 'Customer already in an active Waiting Line'}), 400)

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

def get_next_customer(waiting_line_id):
  
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

def getAll(line_id):
  LineUps = LineUp.query.filter_by(waiting_line_id=line_id).all()
  if not LineUps:
      return (jsonify({'message': 'No Customers found'}), 200)
  resp = {'data': []} 
  for line_up in LineUps:
      resp['data'].append( {  'id': line_up.id,
                              'customer_id': line_up.customer_id,
                              'waiting_line_id': line_up.waiting_line_id, 
                              'status': line_up.status,
                              'created_at': format_datetime(line_up.created_at),
                              'updated_at': format_datetime(line_up.updated_at)})
  response = flask.make_response(jsonify(resp), 200)
  
  response.headers["Content-Type"] = "application/json"
  return response

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
          line_up.cancelled_at = datetime.now()
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
                                      'completed_at': format_datetime(line_up.completed_at),
                                      'cancelled_at': format_datetime(line_up.cancelled_at),
                                      'status': line_up.status}}), 200)
  response.headers["Content-Type"] = "application/json"
  return response