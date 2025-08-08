import os

class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:Vjkjmsgjhrmjn_7@localhost/smart_recruiter"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')
