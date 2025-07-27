from datetime import datetime
from backend.app import db
from sqlalchemy_serializer import SerializerMixin

class Question(db.Model,SerializerMixin):
    __tablename__='questions'

    id=db.Column(db.Integer,primary_key=True)
    assessment_id=db.Column(db.Integer,db.ForeignKey('assessments.id'),nullable=False)
    question_text=db.Column(db.Text,nullable=False)
    question_type=db.Column(db.String(75),nullable=False)
    content=db.Column(db.Text,nullable=False)
    options=db.Column(db.JSON,nullable=True)
    correct_answer=db.Column(db.String,nullable=True)
    created_at=db.Column(db.DateTime,default=datetime.utcnow)
    parent_id=db.Column(db.Integer,db.ForeignKey('questions.id'))

    
    parent=db.relationship("Question",remote_side=[id])
    assessment = db.relationship("Assessment", back_populates="questions")

    serialize_rules=('-assessment.questions','-responses.question',)
