from backend.app import db
from sqlalchemy_serializer import SerializerMixin

class Submission(db.Model, SerializerMixin):
    __tablename__ = 'submissions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) 
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessments.id'), nullable=False)
    invitation_id = db.Column(db.Integer, db.ForeignKey('invitations.id'), nullable=True)
    code = db.Column(db.Text, nullable=True)
    score = db.Column(db.Float, nullable=True)
    status = db.Column(db.String(50), default='submitted')
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    candidate = db.relationship('User', backref='submissions')
    assessment = db.relationship('Assessment', backref='submissions')
    invitation = db.relationship('Invitation', backref='submissions')

    serialize_rules = ('-candidate.password', '-assessment.submissions', '-invitation.submissions')
