from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class Config(db.Model):
    __tablename__ = 'config'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    company_configs = db.relationship('CompanyConfig', backref='config', lazy=True)


