from backend.app import db
from sqlalchemy_serializer import SerializerMixin

class Question(db.Model, SerializerMixin):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(50)) 
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessments.id'), nullable=False)
    
    assessment = db.relationship('Assessment', back_populates='questions')

    serialize_rules = ('-assessment.questions',)
