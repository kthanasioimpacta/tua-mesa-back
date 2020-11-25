from datetime import datetime
import flask
from flask import jsonify
from app import db
from sqlalchemy import and_

from app.shared.Util import format_datetime
from app.models.Customer import Customer

def save(data): 
  name = data['name']
  if 'phone_region' not in data:
      phone_region = '+55'
  else:
      phone_region = data['phone_region']
  phone_number=data['phone_number']
  description = None
  if 'description' in data:
      description = data['description']
  email = None
  if 'email' in data:
      email = data['email']
  customer = Customer.query.filter(and_(Customer.phone_region==phone_region,Customer.phone_number==phone_number)).first()
  if customer is not None:
      response = flask.make_response(jsonify({ 'data': {
                                      'id': customer.id,
                                      'name': customer.name, 
                                      'phone_region': customer.phone_region,
                                      'phone_number': customer.phone_number,
                                      'description': description,
                                      'email': email,
                                      'status': customer.status,
                                      'created_at': format_datetime(customer.created_at),
                                      'updated_at': format_datetime(customer.updated_at)}}), 201)
      response.headers["Content-Type"] = "application/json"
      return response

  customer = Customer(name=name,
              phone_number=phone_number, 
              phone_region=phone_region, 
              description=description,
              email=email,
              status=1, # ATIVO
              created_at=datetime.now(),
              updated_at=datetime.now())
  # user.hash_password(data['password'])
  db.session.add(customer)
  db.session.commit()

  response = flask.make_response(jsonify({ 'data': {
                                      'id': customer.id,
                                      'name': customer.name, 
                                      'phone_region': customer.phone_region,
                                      'phone_number': customer.phone_number,
                                      'description': description,
                                      'email': email,
                                      'status': customer.status,
                                      'created_at': format_datetime(customer.created_at),
                                      'updated_at': format_datetime(customer.updated_at)}}), 201)
  response.headers["Content-Type"] = "application/json"
  return response


def get(id):
  customer = Customer.query.get(id)
  if not customer:
      return (jsonify({'message': 'Customer not found'}), 404)
  
  response = flask.make_response(jsonify({ 'data': {
                                      'id': customer.id,
                                      'name': customer.name, 
                                      'phone_region': customer.phone_region,
                                      'phone_number': customer.phone_number,
                                      'description': customer.description,
                                      'email': customer.email,
                                      'status': customer.status,
                                      'created_at': format_datetime(customer.created_at),
                                      'updated_at': format_datetime(customer.updated_at)}}), 200)
  response.headers["Content-Type"] = "application/json"
  return response