from backend.app import db
import datetime
from sqlalchemy_serializer import SerializerMixin

class Question(db.Model, SerializerMixin):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessments.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(50), default='multiple_choice')  # or 'coding', 'short_answer', etc.
    options = db.Column(db.JSON)  # For MCQ options, null otherwise
    correct_answer = db.Column(db.String(500))  # Optional, used by recruiter for scoring
    points = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    assessment = db.relationship('Assessment', back_populates='questions')

    def serialize(self):
        return {
            "id": self.id,
            "assessment_id": self.assessment_id,
            "text": self.text,
            "question_type": self.question_type,
            "options": self.options,
            "correct_answer": self.correct_answer,
            "points": self.points,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
