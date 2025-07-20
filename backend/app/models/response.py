from datetime import datetime
from backend.app import db
from sqlalchemy_serializer import SerializerMixin

class Response(db.Model,SerializerMixin):
    __tablename__='responses'

    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)
    assessment_id=db.Column(db.Integer,db.ForeignKey('assessments.id'),nullable=False)
    submitted_at=db.Column(db.DateTime,default=datetime.utcnow)
    score=db.Column(db.Float,nullable=True)
    feedback=db.Column(db.Text,nullable=True)
    duration_seconds=db.Column(db.Integer,nullable=True)
    execution_seconds=db.Column(db.Float,nullable=True)
    language_used=db.Column(db.String(50),nullable=True)
    status=db.Column(db.String(20),default='pending')
    passed=db.Column(db.Boolean,nullable=True)
    code_submission=db.Column(db.Text,nullable=True)
    graded_at=db.Column(db.DateTime,nullable=True)
    answer_text=db.Column(db.Text,nullable=True)



    def __repr__(self):
        return f"<Response id={self.id},user_id={self.user_id},score={self.score},assessment_id={self.assessment_id},passed={self.passed}>"