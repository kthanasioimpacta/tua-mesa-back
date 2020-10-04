from app import db
from sqlalchemy import and_
from datetime import datetime
import flask
from flask import jsonify

from app.shared.Util import format_datetime
from app.models.Company import Company

def save(data):
  name = data['name']
  if 'phone_region' not in data:
      phone_region = '+55'
  else:
      phone_region = data['phone_region']
  phone_number=data['phone_number']
  company = Company(  name=name,
                      phone_number=phone_number, 
                      phone_region=phone_region, 
                      status=1, # ATIVO
                      created_at=datetime.now(),
                      updated_at=datetime.now())

  if company.query.filter(and_(Company.phone_region==phone_region,Company.phone_number==phone_number)).first() is not None:
      return (jsonify({'message': 'Company already exists'}), 400)

  db.session.add(company)
  db.session.commit()

  response = flask.make_response(jsonify({ 'data': {
                                        'id': company.id,
                                        'name': company.name, 
                                        'phone_region': company.phone_region,
                                        'phone_number': company.phone_number,
                                        'status': company.status,
                                        'created_at': format_datetime(company.created_at),
                                        'updated_at': format_datetime(company.updated_at)}}), 201)
  response.headers["Content-Type"] = "application/json"
  return response

def get(id):
  company = Company.query.get(id)
  if not company:
      return (jsonify({'message': 'Company not found'}), 404)
  
  response = flask.make_response(jsonify({ 'data': {
                                      'id': company.id,
                                      'name': company.name, 
                                      'phone_region': company.phone_region,
                                      'phone_number': company.phone_number,
                                      'admin_email': company.admin_email,
                                      'status': company.status,
                                      'created_at': format_datetime(company.created_at),
                                      'updated_at': format_datetime(company.updated_at)}}), 200)
  response.headers["Content-Type"] = "application/json"
  return response