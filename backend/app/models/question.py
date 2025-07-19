from datetime import datetime
from backend.app import db
from sqlalchemy_serializer import SerializerMixin

class Question(db.Model,SerializerMixin):
    __tablename__='questions'

    id=db.Column(db.Integer,primary_key=True)

    question=db.Column(db.String(275),nullable=False)
    question_type=db.Column(db.String(100),default='multiple_choice',nullable=False)
    correct_answer=db.Column(db.String(250),nullable=True)
    mark=db.Column(db.Integer,nullable=False)
    difficulty=db.Column(db.String(50))
    input_format=db.Column(db.Text)
    output_format=db.Column(db.Text)
    sample_input=db.Column(db.Text)
    sample_output=db.Column(db.Text)
    constraints=db.Column(db.Text)
    assessment_id=db.Column(db.Integer,db.ForeignKey('assessments.id'),nullable=False)
    tags=db.Column(db.String(300))
    created_at=db.Column(db.DateTime,default=datetime.utcnow)
    updated_at=db.Column(db.DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)
    
    

    choices=db.relationship('Choice',backref='question',lazy='select',cascade='all,delete-orphan')


    def __repr__(self):
        return f"<Question id={self.id},question_type={self.question_type},difficulty={self.difficulty},marks={self.marks}>"
