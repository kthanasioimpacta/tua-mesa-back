import flask
from flask import jsonify,g, current_app
from app import db
from sqlalchemy import or_, and_
import time
from datetime import datetime

from app.shared.Util import format_datetime
from app.shared.SetCookie import setCookie
from app.models.Company import Company
from app.models.User import User

from app.shared.Authentication import verify_password

def save(data):
  username = data['username']
  email = data['email']
  if 'phone_region' not in data:
      phone_region = '+55'
  else:
      phone_region = data['phone_region']

  if User.query.filter(or_(User.email==email,User.username==username)).first() is not None:
      return (jsonify({'message': 'User already exists'}), 400)

  user = User(username=username, 
              email=email, 
              company_id=data['company_id'], 
              phone_number=data['phone_number'], 
              phone_region=phone_region, 
              role_id=data['role_id'], 
              status=1, # ATIVO
              created_at=datetime.now(),
              updated_at=datetime.now())

  user.hash_password(data['password'])
  if data['role_id'] == 1: # ADMIN
      company = Company.query.get(data['company_id'])
      company.admin_email = data['email']
      db.session.add(company)

  db.session.add(user)
  db.session.commit()

  verify_password(user.username, data['password'])
  token = g.user.generate_auth_token(current_app.config['TOKEN_TTL'])
  response = flask.make_response(jsonify({ 'data': {
                                      'id': user.id,
                                      'username': user.username, 
                                      'company_id': user.company_id,
                                      'email': user.email,
                                      'phone_region': user.phone_region,
                                      'phone_number': user.phone_number,
                                      'status': user.status,
                                      'role_id': user.role_id,
                                      'created_at': format_datetime(user.created_at),
                                      'updated_at': format_datetime(user.updated_at)}}), 201)
  response.headers["Content-Type"] = "application/json"
  response = setCookie(response,token)
  return response

def get(id):
  user = User.query.filter(and_(User.id==id,User.company_id==g.user.company_id)).first()
  if not user:
    return (jsonify({'message': 'User not found'}), 404)
  response = flask.make_response(jsonify({ 'data': {
                                        'id': user.id,
                                        'username': user.username, 
                                        'company_id': user.company_id,
                                        'email': user.email,
                                        'phone_region': user.phone_region,
                                        'phone_number': user.phone_number,
                                        'status': user.status,
                                        'role_id': user.role_id,
                                        'created_at': format_datetime(user.created_at),
                                        'updated_at': format_datetime(user.updated_at)}}), 200)
  response.headers["Content-Type"] = "application/json"
  return response

def get_auth_token(data):
  company = Company.query.get(g.user.company_id)

  if data['email'] != company.admin_email:
      return (jsonify({'message': 'Not Authorized' })), 401

  token = g.user.generate_auth_token(current_app.config['TOKEN_TTL'])

  response = flask.make_response(jsonify({ 'data': {
                                      'id': g.user.id,
                                      'username': g.user.username, 
                                      'company_id': g.user.company_id,
                                      'email': g.user.email,
                                      'phone_region': g.user.phone_region,
                                      'phone_number': g.user.phone_number,
                                      'status': g.user.status,
                                      'role_id': g.user.role_id,
                                      'created_at': format_datetime(g.user.created_at),
                                      'updated_at': format_datetime(g.user.updated_at)}}), 200)
  response.headers["Content-Type"] = "application/json"
  
  setCookie(response,token)
  return response

def get_current_user():
  return flask.make_response({ 'data': {
                                        'id': g.user.id,
                                        'username': g.user.username, 
                                        'company_id': g.user.company_id,
                                        'email': g.user.email,
                                        'phone_region': g.user.phone_region,
                                        'phone_number': g.user.phone_number,
                                        'status': g.user.status,
                                        'role_id': g.user.role_id,
                                        'created_at': format_datetime(g.user.created_at),
                                        'updated_at': format_datetime(g.user.updated_at)}}, 200)

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