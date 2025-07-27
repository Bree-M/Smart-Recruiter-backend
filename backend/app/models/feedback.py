from backend.app import db
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin

class Feedback(db.Model,SerializerMixin):
    __tablename__='feedback'

    id=db.Column(db.Integer,primary_key=True)
    response_id=db.Column(db.Integer,db.ForeignKey('responses.id'),nullable=False)
    comment=db.Column(db.Text,nullable=False)
    created_at=db.Column(db.DateTime,default=datetime.utcnow)
    recruiter_id=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)

    response=db.relationship('Response',backref='feedbacks')
    recruiter=db.relationship('User',backref='given_feedbacks')

    serialize_rules=('-response.feedbacks','-recruiter.given_feedbacks')
