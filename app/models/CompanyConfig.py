from app import db

class CompanyConfig(db.Model):
    __tablename__ = 'company_config'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"), index=True, nullable=False) 
    config_id = db.Column(db.Integer, db.ForeignKey("config.id"), index=True, nullable=False) 
    value = db.Column(db.String(1024), index=False, nullable=False, unique=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    

