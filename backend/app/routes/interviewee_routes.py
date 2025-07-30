from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from backend.app.models import db, Invitation, Response,Submission,Result,Feedback

interviewee_bp = Blueprint('interviewee', __name__, url_prefix='/interviewee')

@interviewee_bp.route('/invitations', methods=['GET'])
@jwt_required()
def get_invitations():
    user_id = get_jwt_identity()['id']
    invitations = Invitation.query.filter_by(interviewee_id=user_id).all()
    return jsonify([i.serialize() for i in invitations]), 200

@interviewee_bp.route('/submit', methods=['POST'])
@jwt_required()
def submit_assessment():
    data = request.get_json()
    user_id=get_jwt_identity()['id']
    if not data.get('assessment_id') or data.get('answers'):
        return jsonify({'error':'assessment_id and answers required'}),400
    submission = Submission(
        interviewee_id=user_id,
        assessment_id=data['assessment_id'],
        answers=data['answers'],
        submitted_at=datetime.utcnow()
    )
    db.session.add(submission)
    db.session.commit()
    return jsonify({'message': 'Assessment submitted','submission':submission.serialize()}), 201

@interviewee_bp.route('/submissions',methods=['GET'])
@jwt_required()
def get_my_submissions():
    user_id=get_jwt_identity()['id']
    submissions=Submission.query.filter_by(interviewee_id=user_id).all()
    return jsonify([s.serialize() for s in submissions]),200

@interviewee_bp.route('/responses/<int:submission_id>', methods=['GET'])
@jwt_required()
def view_responses(submission_id):
    user_id=get_jwt_identity()['id']
    submission=Submission.query.filter_by(id=submission_id,interviewee_id=user_id).first()
    if not submission:
        return jsonify({'error':'Submission Not Found!'}),404
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
    return jsonify({'message':'Submissions Updated.','submission':submission.serialize()}),200

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


@interviewee_bp.route('/results',methods=['GET'])
@jwt_required()
def view_my_results():
    user_id=get_jwt_identity()['id']
    results=Result.query.filter_by(interviewee_id=user_id,released=True).all()
    return jsonify([r.serialize() for r in results]),200

@interviewee_bp.route('/feedback/<int:submission_id>',methods=['GET'])
@jwt_required()
def view_feedback(submission_id):
    user=get_jwt_identity()
    submission=Submission.query.filter_by(id=submission_id,interviewee_id=user['id']).first()
    if not submission:
        return jsonify({'error':'Submission Not Found!'}),404
    feedbacks=Feedback.query.filter_by(submission_id=submission_id).all()
    return jsonify([f.serialize()  for f in feedbacks]),200
    
