from backend.app import db
from sqlalchemy_serializer import SerializerMixin

class Invitation(db.Model, SerializerMixin):
    __tablename__ = 'invitations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  
    candidate_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) 
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessments.id'), nullable=False)
    status = db.Column(db.String(50), default='pending')
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    recruiter = db.relationship('User', foreign_keys=[user_id], backref='sent_invitations')
    candidate = db.relationship('User', foreign_keys=[candidate_id], backref='received_invitations')
    assessment = db.relationship('Assessment', backref='invitations')

    serialize_rules = ('-recruiter.password', '-candidate.password', '-assessment.invitations')
