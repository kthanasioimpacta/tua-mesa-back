from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_httpauth import HTTPBasicAuth
from flask import current_app
import jwt
import time
from datetime import datetime

auth = HTTPBasicAuth()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"), index=True, nullable=False) 
    username = db.Column(db.String(32), index=True, nullable=False, unique=True)
    phone_region = db.Column(db.String(5), index=False, nullable=False)
    phone_number = db.Column(db.String(100), index=False, nullable=False)
    email = db.Column(db.String(100), index=True, nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    role_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    def hash_password(self, password):
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def generate_auth_token(self, expires_in=600):
        payload = {'id': self.id, 'exp': time.time() + expires_in}
        return jwt.encode(
            payload,
            current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_auth_token(token):
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'],
                              algorithms=['HS256'])
        except:
            return
        return User.query.get(data['id'])

@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True
