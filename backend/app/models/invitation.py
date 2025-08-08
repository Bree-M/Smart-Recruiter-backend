from backend.app import db
import datetime
from sqlalchemy_serializer import SerializerMixin

class Invitation(db.Model, SerializerMixin):
    __tablename__ = 'invitations'
    
    id = db.Column(db.Integer, primary_key=True)
    recruiter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    candidate_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessments.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')  
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    recruiter = db.relationship('User', foreign_keys=[recruiter_id])
    candidate = db.relationship('User', foreign_keys=[candidate_id])
    assessment = db.relationship('Assessment')

    def serialize(self):
        return {
            "id": self.id,
            "recruiter_id": self.recruiter_id,
            "candidate_id": self.candidate_id,
            "assessment_id": self.assessment_id,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "assessment_title": self.assessment.title if self.assessment else None,
            "candidate_username": self.candidate.username if self.candidate else None,
            "recruiter_username": self.recruiter.username if self.recruiter else None,
        }


