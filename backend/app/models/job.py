from datetime import datetime
from backend.app import db

class Job(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(200), nullable=True)
    employment_type = db.Column(db.String(50), nullable=True)
    salary_range = db.Column(db.String(100), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    recruiter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recruiter = db.relationship('User', backref=db.backref('jobs', lazy='dynamic'))

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "location": self.location,
            "employment_type": self.employment_type,
            "salary_range": self.salary_range,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "recruiter_id": self.recruiter_id,
            "recruiter_username": getattr(self.recruiter, "username", None)
        }
