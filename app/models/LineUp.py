from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class LineUp(db.Model):
    __tablename__ = 'line_up'
    id = db.Column(db.Integer, primary_key=True)
    waiting_line_id = db.Column(db.Integer, db.ForeignKey("waiting_line.id"), index=True, nullable=False) 
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), index=True, nullable=False) 
    joined_at = db.Column(db.DateTime, nullable=False)
    first_call_at = db.Column(db.DateTime, nullable=False)
    second_call_at = db.Column(db.DateTime, nullable=False)
    completed_call_at = db.Column(db.DateTime, nullable=False)
    cancelled_call_at = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    

