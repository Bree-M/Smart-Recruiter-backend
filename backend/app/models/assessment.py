from datetime import datetime
from backend.app import db
from sqlalchemy_serializer import SerializerMixin

class Assessment(db.Model,SerializerMixin):
    __tablename__='assessments'

    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    description=db.Column(db.Text)
    time_limit=db.Column(db.Integer)
    recruiter_id=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    created_at=db.Column(db.DateTime,default=datetime.utcnow)
    updated_at=db.Column(db.DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)
    is_published=db.Column(db.Boolean,default=False)
    category=db.Column(db.String(150))
    difficulty=db.Column(db.String(75))

    questions=db.relationship('Question',backref='assessment',lazy='select',cascade="all,delete-orphan")
    invitations=db.relationship('Invitation',backref='assessment',lazy='select',cascade="all,delete-orphan")

    def __repr__(self):
        return f"<Assessment id={self.id},title='{self.title}'difficulty={self.difficulty},recruiter_id={self.recruiter_id}>"
        l