from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.app.models import db, Invitation, Response,Submission

interviewee_bp = Blueprint('interviewee', __name__, url_prefix='/interviewee')

@interviewee_bp.route('/invitations', methods=['GET'])
@jwt_required()
def get_invitations():
    user = get_jwt_identity()
    invitations = Invitation.query.filter_by(interviewee_id=user['id']).all()
    return jsonify([i.serialize() for i in invitations]), 200

@interviewee_bp.route('/submit', methods=['POST'])
@jwt_required()
def submit_assessment():
    data = request.get_json()
    submission = Submission(
        interviewee_id=get_jwt_identity()['id'],
        assessment_id=data['assessment_id'],
        answers=data['answers'],
        submitted_at=data['submitted_at']
    )
    db.session.add(submission)
    db.session.commit()
    return jsonify({'message': 'Assessment submitted'}), 201

@interviewee_bp.route('/responses/<submission_id>', methods=['GET'])
@jwt_required()
def view_responses(submission_id):
    responses = Response.query.filter_by(submission_id=submission_id).all()
    return jsonify([r.serialize() for r in responses]), 200
