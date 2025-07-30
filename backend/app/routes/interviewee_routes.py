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

@interviewee_bp.route('/invitations/<int:invitation_id>/accept',methods=['PATCH'])
@jwt_required()
def accept_invitation(invitation_id):
    user_id=get_jwt_identity()['id']
    invitation=Invitation.query.filter_by(id=invitation_id,interviewee_id=user_id).first()
    if not invitation:
        return jsonify({'error':'Invitation Not Found!'}),404
    if invitation.status != 'pending':
        return jsonify({'error':f'Cannot accept invitation with status {invitation.status}'}),400
    invitation.status='accepted'
    db.session.commit()
    return jsonify({'message':'Invitationaccepted','invitation':invitation.serialize()}),200

@interviewee_bp.route('/invitations/<int:invitation_id>/decline',method=['PATCH'])
@jwt_required()
def decline_invitation(invitation_id):
    user_id=get_jwt_identity()['id']
    invitation=Invitation.query.filter_by(id=invitation_id,interviewee_id=user_id).first()
    if not invitation:
        return jsonify({'error':'Invitation Not Found!'}),404
    if invitation.status != 'pending':
        return jsonify({'error':f'Cannot Decline Invitation With Status {invitation.status}'}),400
    invitation.status='declined'
    db.session.commit()
    return jsonify({'message':'Invitation Declined','invitation':invitation.serialize()}),200
        
    

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

@interviewee_bp.route('/response/<int:response_id>',methods=['PATCH'])
@jwt_required()
def update_my_response(response_id):
    user=get_jwt_identity()
    response=Response.query.get(response_id)
    if not response:
        return jsonify({'error':'Response Not Found!'}),404
    if response.interviewee_id != user['id']:
        return jsonify({'error':'Authorization Required!'}),403
    if response.submission.status == 'submitted':
        return jsonify({'error':'Cannot Edit Response!'}),403
    data=request.get_json()
    if 'answer_text' in data:
        response.answer_text=data['answer_text']

    db.session.commit()    
    return jsonify({'message':'Response Updated','response':response.serialize()}),200

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
    submission=Submission.query.filter_by(id=submission_id,interviewee_id=user_id).first()
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
    
