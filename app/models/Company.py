from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class Company(db.Model):
    __tablename__ = 'company'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True)
    phone_region = db.Column(db.String(5), index=False, nullable=False)
    phone_number = db.Column(db.String(100), index=False, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    users = db.relationship('User', backref='company', lazy=True)
    waiting_lines = db.relationship('WaitingLine', backref='company', lazy=True)
    company_configs = db.relationship('CompanyConfig', backref='company', lazy=True)

    __table_args__ = (db.UniqueConstraint('phone_region', 'phone_number', name='_company_uc'),
                     )


