from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class WaitingLine(db.Model):
    __tablename__ = 'waiting_line'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"), index=True, nullable=False) 
    status = db.Column(db.Integer, nullable=False)
    is_priority = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    line_ups = db.relationship('LineUp', backref='waiting_line', lazy=True)
    __table_args__ = (db.UniqueConstraint('company_id', 'name', name='_company_wait_line_uc'),)


