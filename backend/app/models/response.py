from backend.app import db
from sqlalchemy_serializer import SerializerMixin

class Response(db.Model, SerializerMixin):
    __tablename__ = 'responses'

    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, db.ForeignKey('submissions.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    answer = db.Column(db.Text, nullable=True)
    score = db.Column(db.Float, nullable=True)
    feedback = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    submission = db.relationship('Submission', backref='responses')
    question = db.relationship('Question', backref='responses')

    serialize_rules = ('-submission.responses', '-question.responses')
