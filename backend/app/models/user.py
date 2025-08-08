from backend.app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'


    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(200),nullable=False,unique=True)
    email=db.Column(db.String(200),nullable=False,unique=True)
    password=db.Column(db.String(200),nullable=False)
    role=db.Column(db.String(50),nullable=False)
    created_at=db.Column(db.DateTime,default=datetime.utcnow)
    about_me=db.Column(db.Text)
    profile_picture_url=db.Column(db.String(120))
    bio=db.Column(db.Text)
    company_name=db.Column(db.String(300))
    skills=db.Column(db.String)
    password_hash=db.Column(db.String,nullable=False)

    assessments=db.relationship('Assessment',backref='recruiter',lazy='select')
    


    def set_password(self,password):
        self.password=generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password,password)

    serialize_rules=('-password','-password_hash','-assessments.recruiter','-invitations.interviewee','-submissions.interviewee','-submissions.assessment.recruiter')


