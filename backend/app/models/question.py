from backend.app import db
import datetime
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.dialects.postgresql import JSON

class Question(db.Model, SerializerMixin):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessments.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(50), nullable=False) 
    choices = db.Column(JSON, nullable=True)  
    correct_answer = db.Column(db.Text, nullable=True)  
    points = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    assessment = db.relationship('Assessment', back_populates='questions')

    def serialize(self):
        return {
            "id": self.id,
            "assessment_id": self.assessment_id,
            "question_text": self.question_text,
            "question_type": self.question_type,
            "choices": self.choices,
            "correct_answer": self.correct_answer,
            "points": self.points,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

