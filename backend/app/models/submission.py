from backend.app import db
import datetime
from sqlalchemy_serializer import SerializerMixin

class Submission(db.Model, SerializerMixin):
    __tablename__ = 'submissions'

    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessments.id'), nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    status = db.Column(db.String(50), default='submitted')  
    score = db.Column(db.Float)  

    candidate = db.relationship('User', foreign_keys=[candidate_id])
    assessment = db.relationship('Assessment')
    responses = db.relationship('Response', back_populates='submission', cascade='all, delete', lazy='select')
    result = db.relationship('Result', back_populates='submission', uselist=False)
    feedbacks = db.relationship('Feedback', back_populates='submission', cascade='all, delete-orphan')


    def serialize(self):
        return {
            'id': self.id,
            'candidate_id': self.candidate_id,
            'candidate_username': self.candidate.username if self.candidate else None,
            'assessment_id': self.assessment_id,
            'assessment_title': self.assessment.title if self.assessment else None,
            'submitted_at': self.submitted_at.isoformat() if self.submitted_at else None,
            'status': self.status,
            'score': self.score,
            'responses': [response.serialize() for response in self.responses]
        }
