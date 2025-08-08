from backend.app import db
from sqlalchemy_serializer import SerializerMixin

class Feedback(db.Model, SerializerMixin):
    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key=True)
    response_id = db.Column(db.Integer, db.ForeignKey('responses.id'), nullable=False)
    recruiter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    response = db.relationship('Response', backref=db.backref('feedback_entries', lazy=True, cascade="all, delete-orphan"))
    recruiter = db.relationship('User', backref=db.backref('feedback_given', lazy=True))

    serialize_rules = ('-recruiter.password', '-recruiter.feedback_given', '-response.feedback')
