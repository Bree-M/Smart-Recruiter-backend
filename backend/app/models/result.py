from backend.app import db
from sqlalchemy_serializer import SerializerMixin

class Result(db.Model, SerializerMixin):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, db.ForeignKey('submissions.id'), nullable=False, unique=True)
    total_score = db.Column(db.Float, nullable=True)
    percentage = db.Column(db.Float, nullable=True)
    status = db.Column(db.String(50), nullable=True)
    feedback = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    submission = db.relationship('Submission', backref=db.backref('result', uselist=False))

    serialize_rules = ('-submission.result',)
