from backend.app import db
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin

class User(db.Model,SerializerMixin):
    __tablename__='users'

    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(120),unique=True, nullable=False)
    email=db.Column(db.String(150),unique=True,nullable=False)
    password_hash=db.Column(db.String(600),nullable=False)
    role=db.Column(db.String(20),nullable=False)
    profile_picture_url=db.Column(db.String(250),nullable=True)
    bio=db.Column(db.Text,nullable=True)
    about_me=db.Column(db.Text,nullable=True)
    company_name=db.Column(db.String(150),nullable=True)
    skills=db.Column(db.Text,nullable=True)
    is_active=db.Column(db.Boolean,default=True)
    created_at=db.Column(db.DateTime,default=datetime.utcnow)
    updated_at=db.Column(db.DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)


    assessments=db.relationship('Assessment',backref='recruiter',lazy='select')
    responses=db.relationship('Response',backref='user',lazy='select')

    def set_password(self,password):
        self.password_hash= generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password) 
  

    def __repr__(self):
        return f"<User id={self.id},username='{self.username}',email='{self.email}',role='{self.role}>"
    
