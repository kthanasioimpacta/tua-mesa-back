from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True)
    phone_region = db.Column(db.String(5), index=False, nullable=False)
    phone_number = db.Column(db.String(100), index=False, nullable=False)
    description = db.Column(db.String(100), index=False, nullable=True)
    email = db.Column(db.String(100), index=False, nullable=True)
    status = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    line_ups = db.relationship('LineUp', backref='customer', lazy=True)


