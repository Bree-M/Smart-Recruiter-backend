from backend.app import db
import datetime
from sqlalchemy_serializer import SerializerMixin

class Result(db.Model, SerializerMixin):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, db.ForeignKey('submissions.id'), nullable=False, unique=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessments.id'), nullable=False)
    score = db.Column(db.Float, nullable=False)
    feedback = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    submission = db.relationship('Submission', back_populates='result')
    candidate = db.relationship('User')
    assessment = db.relationship('Assessment')

    def serialize(self):
        return {
            "id": self.id,
            "submission_id": self.submission_id,
            "candidate_id": self.candidate_id,
            "assessment_id": self.assessment_id,
            "score": self.score,
            "feedback": self.feedback,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
