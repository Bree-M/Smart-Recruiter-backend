from backend.app import db
from sqlalchemy_serializer import SerializerMixin

class Result(db.Model,SerializerMixin):
    __tablename__='results'


    id=db.Column(db.Integer,primary_key=True)
    submission_id=db.Column(db.Integer,db.ForeignKey('submissions.id'),nullable=False)
    total_score=db.Column(db.Float,nullable=False)
    max_score=db.Column(db.Float,nullable=False)
    grade=db.Column(db.String(10))
    released=db.Column(db.Boolean,default=False)
    feedback_summary=db.Column(db.Text)

    submission=db.relationship('Submission',backref='result')

    serialize_rules=('-submission.result')




