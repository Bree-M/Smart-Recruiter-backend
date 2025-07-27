from backend.app import db
from sqlalchemy_serializer import SerializerMixin

class Response(db.Model, SerializerMixin):
    __tablename__ = 'responses'

    id=db.Column(db.Integer,primary_key=True)
    interviewee_id=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    recruiter_id=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=True)
    submission_id=db.Column(db.Integer,db.ForeignKey('submissions.id'),nullable=False)
    question_id=db.Column(db.Integer,db.ForeignKey('questions.id'),nullable=False)
    answer_text=db.Column(db.Text,nullable=False)
    is_correct=db.Column(db.Boolean)
    score_awarded=db.Column(db.Integer)

    # submisison=db.relationship('Submission',backref='responses')
    # question=db.relationship('Question',backref='responses')

    serialize_rules=('-submission',)



