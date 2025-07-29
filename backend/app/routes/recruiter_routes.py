from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.app.models import db, Invitation, Response,Result,Submission

recruiter_bp = Blueprint('recruiter', __name__, url_prefix='/recruiter')

@recruiter_bp.route('/invite', methods=['POST'])
@jwt_required()
def send_invitation():
    data = request.get_json()
    invitation = Invitation(
        interviewee_id=data['interviewee_id'],
        assessment_id=data['assessment_id'],
        status='pending'
    )
    db.session.add(invitation)
    db.session.commit()
    return jsonify({'message': 'Invitation sent'}), 201

@recruiter_bp.route('/response', methods=['POST'])
@jwt_required()
def give_feedback():
    data = request.get_json()
    response = Response(
        question_id=data['question_id'],
        submission_id=data['submission_id'],
        recruiter_id=get_jwt_identity()['id'],
        comment=data['comment']
    )
    db.session.add(response)
    db.session.commit()
    return jsonify({'message': 'Response submitted'}), 201

@recruiter_bp.route('/results', methods=['PATCH'])
@jwt_required()
def release_results():
    data = request.get_json()
    result = Result.query.get(data['result_id'])
    if result:
        result.released = True
        db.session.commit()
        return jsonify({'message': 'Results released'}), 200
    return jsonify({'error': 'Result not found'}), 404


@recruiter_bp.route('/submissions',methods=['GET'])
@jwt_required()
def get_my_submissions():
    user_id=get_jwt_identity()['id']
    submissions=Submission.query.filter_by(interviewee_id=user_id).all()
    return jsonify([s.serialize() for s in submissions]),200

@recruiter_bp.route('/submissions/<int:submission_id>',methods=['GET'])
@jwt_required()
def get_submission(submission_id):
    user_id=get_jwt_identity()['id']
    submission=Submission.query.filter_by(id=submission_id,interviewee_id=user_id).first()
    if not submission:
        return jsonify({'error':'Submission not found!'}),404
    return jsonify(submission.serialize()),200

