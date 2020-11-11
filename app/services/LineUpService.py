import re
import flask
import jwt
from flask import jsonify, request
from app import db
from flask import current_app
from sqlalchemy import and_, func
from datetime import datetime
from app.shared.Util import format_datetime
from app.services.SendSMS import SendSMS

from app.shared.Authentication import is_logged, is_admin

from app.models.LineUp import LineUp
from app.models.Customer import Customer

def SendSms(customer_id, message):
  customer = Customer()
  cust = customer.query.filter(and_(Customer.id==customer_id)).first()
  phone_number = cust.phone_number + cust.phone_number
  phone_number = re.compile(r'^[-+]?([1-9]\d*|0)$')
  body = f'{cust.name} - ' + message
  SendSMS(phone_number, body)

def save(data):
  customer = Customer()
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
  token = jwt.encode(
            { 'waiting_line_id': line_up.waiting_line_id, 'line_up_id': line_up.id},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')
  print(token)
  print(str(token))
  body = 'Acompanhe a sua posição na fila de espera: http://www.tuamesa.com.br:8080/api/waiting-lines/position?token={}'.format(str(token))
  SendSms(line_up.customer_id, body)
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
  line_up = LineUp()
  LineUps = line_up.query.filter(and_(LineUp.waiting_line_id==line_id,LineUp.status < 3)).order_by(db.asc('joined_at')).all()
  total = line_up.query.filter(and_(LineUp.waiting_line_id==line_id,LineUp.status < 3)).count()
  
  if not LineUps:
      return (jsonify({'message': 'No Customers found'}), 200)
  resp = {'data': [],'summary': {}} 
  lowest = None
  for line_up in LineUps:
      if (lowest is None):
        lowest = round(((datetime.now() - line_up.joined_at).total_seconds())/60)
      customer = Customer()
      customer_data = customer.query.filter_by(id=line_up.customer_id).first()
      resp['data'].append( {  'id': line_up.id,
                              'customer_id': line_up.customer_id,
                              'customer_name': customer_data.name,
                              'customer_phone_number': customer_data.phone_number,
                              'waiting_line_id': line_up.waiting_line_id, 
                              'status': line_up.status,
                              'joined_at': format_datetime(line_up.joined_at),
                              'first_call_at': format_datetime(line_up.first_call_at),
                              'second_call_at': format_datetime(line_up.second_call_at),
                              'cancelled_at': format_datetime(line_up.cancelled_at),
                              'completed_at': format_datetime(line_up.completed_at)})
  resp['summary'] = {'qty_total': total, 'max_waiting_minutes': lowest}
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
  body = 'Sua mesa está disponível!'
  SendSms(line_up.customer_id, body)
  response.headers["Content-Type"] = "application/json"
  return response