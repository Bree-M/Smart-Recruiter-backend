from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
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

@interviewee_bp.route('/submissions/<int:submission_id>',methods=['PUT'])
@jwt_required()
def update_submission(submission_id):
    user_id=get_jwt_identity()['id']
    submission=Submission.query.filter_by(id=submission_id,interviewee_id=user_id).first()
    if not submission:
        return jsonify({'error':'Submission not found!'}),404
    
    data=request.get_json()
    submission.answers=data.get('answers',submission.answers)
    db.session.commit()
    return jsonify({'message':'Submissions Updated.'}),200

@interviewee_bp.route('/submissions/<int:submission_id>',methods=['DELETE'])
@jwt_required()
def delete_submission(submission_id):
    user_id=get_jwt_identity()['id']
    submission=Submission.query.filter_by(id=submission_id,interviwee_id=user_id).first()
    if not submission:
        return jsonify({'error':'Submission Not Found!'}),404
    
    db.session.delete(submission)
    db.session.commit()
    return jsonify({'message':'Submission Deleted.'}),200
    
