from backend.app import db
import datetime
from sqlalchemy_serializer import SerializerMixin

class Feedback(db.Model, SerializerMixin):
    __tablename__ = 'feedbacks'

    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, db.ForeignKey('submissions.id'), nullable=False)
    recruiter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    submission = db.relationship('Submission', back_populates='feedbacks')
    recruiter = db.relationship('User')

    def serialize(self):
        return {
            "id": self.id,
            "submission_id": self.submission_id,
            "recruiter_id": self.recruiter_id,
            "comment": self.comment,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
