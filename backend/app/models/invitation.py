from datetime import datetime,timedelta
from backend.app import db
from sqlalchemy_serializer import SerializerMixin
import secrets

class Invitation(db.Model,SerializerMixin):
    __tablename__='invitations'

    id=db.Column(db.Integer,primary_key=True)
    recruiter_id=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    interviewee_id=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    assessment_id=db.Column(db.Integer,db.ForeignKey('assessments.id'),nullable=False)
    status=db.Column(db.String(75),default='pending')
    token=db.Column(db.String(150),unique=True,nullable=False,default=lambda: secrets.token_urlsafe(20))
    expiration=db.Column(db.DateTime,default=lambda: datetime.utcnow() + timedelta(days=7)) 
    created_at=db.Column(db.DateTime,default=datetime.utcnow)
    sent_at=db.Column(db.DateTime,default=datetime.utcnow)
    scheduled_at=db.Column(db.DateTime,nullable=True,default=None)


    recruiter=db.relationship('User',foreign_keys=[recruiter_id],backref='sent_invitations')
    interviewee=db.relationship('User',foreign_keys=[interviewee_id],backref='received_invitations')

    serialize_rules=('-assessment.invitations','-recruiter.sent_invitations','-interviewee.received_invitations')



