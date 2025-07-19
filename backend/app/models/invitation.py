from datetime import datetime
from backend.app import db
from sqlalchemy_serializer import SerializerMixin
import secrets

class Invitation(db.Model,SerializerMixin):
    __tablename__='invitations'

    id=db.Column(db.Integer,primary_key=True)
    assessment_id=db.Column(db.Integer,db.ForeignKey('assessments.id'),nullable=False)
    interviewee_id=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    recruiter_id=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=True)
    status=db.Column(db.String(50),default='pending')
    token=db.Column(db.String(300),unique=True,index=True,default=lambda:secrets.token_urlsafe(50))
    token_used_at=db.Column(db.DateTime,nullable=True)
    is_active=db.Column(db.Boolean,default=True)
    invited_via=db.Column(db.String(50),default='email')
    invitation_message=db.Column(db.Text,nullable=True)
    sent_at=db.Column(db.DateTime,default=datetime.utcnow)
    resend_count=db.Column(db.Integer,default=0)
    last_resent_at=db.Column(db.DateTime,nullable=True)
    revoked=db.Column(db.Boolean,default=False)
    time_taken_seconds=db.Column(db.Integer,nullable=True)
    expires_at=db.Column(db.DateTime,nullable=True)
    started_at=db.Column(db.DateTime,nullable=True)
    completed_at=db.Column(db.DateTime,nullable=True)
    score=db.Column(db.Integer,nullable=True)
    feedback=db.Column(db.Text,nullable=True)

    interviewee=db.relationship('User',foreign_keys=[interviewee_id])
    recruiter=db.relationship('User',foreign_keys=[recruiter_id])
    assessment=db.relationship('Assessment',foreign_keys=[assessment_id])

    def __repr__(self):
        return (
            f"<Invitation id={self.id},interviewee_id={self.interviewee_id},"
            f"recruiter_id={self.recruiter_id},assessment_id={self.assessment_id},"
            f"status='{self.status}',sent_at={self.sent_at},expires_at={self.expires_at}>"
        )

