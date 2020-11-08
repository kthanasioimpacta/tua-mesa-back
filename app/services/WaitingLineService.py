import flask
from flask import jsonify, g
from app.models.WaitingLine import WaitingLine

from app import db
from sqlalchemy import and_

from datetime import datetime
from app.shared.Util import format_datetime

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