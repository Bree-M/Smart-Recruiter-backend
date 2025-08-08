from backend.app import db
import datetime
from sqlalchemy_serializer import SerializerMixin

class Response(db.Model, SerializerMixin):
    __tablename__ = 'responses'

    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, db.ForeignKey('submissions.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    answer_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    submission = db.relationship('Submission', back_populates='responses')
    question = db.relationship('Question')

    def serialize(self):
        return {
            'id': self.id,
            'submission_id': self.submission_id,
            'question_id': self.question_id,
            'answer_text': self.answer_text,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'question_text': self.question.text if self.question else None
        }
