import flask
import jwt
from flask import jsonify, g, current_app
from app.models.WaitingLine import WaitingLine
import json
from app import db
from sqlalchemy import and_

from datetime import datetime
from app.shared.Util import format_datetime

from app.models.LineUp import LineUp
from app.models.Company import Company
# from app.models.Customer import Customer

def save(data):
  name = data['name']
  waiting_line = WaitingLine(name=name,
              company_id=g.user.company_id,
              status=1, # ATIVO
              is_priority=data['is_priority'],
              created_at=datetime.now(),
              updated_at=datetime.now())

  if waiting_line.query.filter(and_(WaitingLine.company_id==g.user.company_id,WaitingLine.name==name)).first() is not None:
      return (jsonify({'message': 'Company already exists'}), 400)

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

def getAll():
  waiting_lines = WaitingLine.query.filter_by(company_id=g.user.company_id).all()
  if not waiting_lines:
      return (jsonify({'message': 'No Waiting Lines found'}), 200)
  resp = {'data': [],'summary': {}} 
  for waiting_line in waiting_lines:
      lowest = None
      line_up = LineUp()
      total = line_up.query.filter(and_(LineUp.waiting_line_id==waiting_line.id,LineUp.status < 3)).count()
      line = line_up.query.filter(and_(LineUp.waiting_line_id==waiting_line.id,LineUp.status < 3)).order_by(db.asc('joined_at')).first()
      if (line):
        lowest = round(((datetime.now() - line.joined_at).total_seconds())/60)
      resp['data'].append( {  'id': waiting_line.id,
                              'company_id': waiting_line.company_id,
                              'name': waiting_line.name, 
                              'is_priority': waiting_line.is_priority,
                              'status': waiting_line.status,
                              'created_at': format_datetime(waiting_line.created_at),
                              'updated_at': format_datetime(waiting_line.updated_at),
                              'qty_total': total,
                              'max_waiting_minutes': lowest}
                              )
  response = flask.make_response(jsonify(resp), 200)
  
  response.headers["Content-Type"] = "application/json"
  return response


def get(id):
  waiting_line = WaitingLine.query.filter(and_(WaitingLine.id==id,WaitingLine.company_id==g.user.company_id)).first()
  if not waiting_line:
      return (jsonify({'message': 'No Waiting Line found'}), 200)
  resp = {'data': [],'summary': {}} 
  
  lowest = None
  line_up = LineUp()
  total = line_up.query.filter(and_(LineUp.waiting_line_id==waiting_line.id,LineUp.status < 3)).count()
  line = line_up.query.filter(and_(LineUp.waiting_line_id==waiting_line.id,LineUp.status < 3)).order_by(db.asc('joined_at')).first()
  if (line):
    lowest = round(((datetime.now() - line.joined_at).total_seconds())/60)
  resp['data'].append( {  'id': waiting_line.id,
                          'company_id': waiting_line.company_id,
                          'name': waiting_line.name, 
                          'is_priority': waiting_line.is_priority,
                          'status': waiting_line.status,
                          'created_at': format_datetime(waiting_line.created_at),
                          'updated_at': format_datetime(waiting_line.updated_at),
                          'qty_total': total,
                          'max_waiting_minutes': lowest}
                          )
  response = flask.make_response(jsonify(resp), 200)
  
  response.headers["Content-Type"] = "application/json"
  return response

def getPosition(token):
  data = jwt.decode(token, current_app.config['SECRET_KEY'],
                  algorithms=['HS256'])
  print(data)
  
  waiting_line_id = data['waiting_line_id']
  line_up_id = data[ 'line_up_id']
  
  resp = {'data': [],'summary': {}} 
  line_up = LineUp()
  posicao = line_up.query.filter(and_(LineUp.waiting_line_id==waiting_line_id,LineUp.status < 3,LineUp.id <= line_up_id)).count()
  
  waiting_line = WaitingLine()
  waiting = waiting_line.query.filter(and_(WaitingLine.id == waiting_line_id)).first()
  
  company = Company()
  company = Company.query.filter(and_(Company.id == waiting.company_id)).first()
  
  resp['data'].append( {  'position': posicao,
                          'company_name': company.name,
                          'waiting_line_name': waiting_line.name}
                          )
  response = flask.make_response(jsonify(resp), 200)
  
  response.headers["Content-Type"] = "application/json"
  return response