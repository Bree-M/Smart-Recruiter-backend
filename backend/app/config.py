import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', "postgresql://postgres:password@localhost/smart_recruiter")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'mydefaultjwtsecretkey123')
    JWT_ACCESS_TOKEN_EXPIRES = 43200
