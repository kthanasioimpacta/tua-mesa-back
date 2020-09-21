#!/usr/bin/env python
import flask
from flask import request, g

from flask_httpauth import HTTPBasicAuth
from app.models.User import User

auth = HTTPBasicAuth()

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

def is_logged():
    return verify_password(request.cookies.get('token'))


def is_admin():
    return g.user.role_id == 1
