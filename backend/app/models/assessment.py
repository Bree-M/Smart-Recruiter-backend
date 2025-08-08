from datetime import datetime
from backend.app import db
from sqlalchemy_serializer import SerializerMixin

class Assessment(db.Model, SerializerMixin):
    __tablename__ = 'assessments'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    time_limit = db.Column(db.Integer) 
    description = db.Column(db.Text)
    difficulty = db.Column(db.String(50))
    is_published = db.Column(db.Boolean, default=False)
    category = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    recruiter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    questions = db.relationship(
        'Question', back_populates='assessment', cascade='all, delete', lazy='select'
    )

    serialize_rules = ('-recruiter.assessments', '-questions.assessment', '-invitations.assessment')

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'time_limit': self.time_limit,
            'description': self.description,
            'difficulty': self.difficulty,
            'is_published': self.is_published,
            'category': self.category,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'recruiter_id': self.recruiter_id,
        }
