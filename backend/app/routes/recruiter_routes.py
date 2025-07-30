from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.app.models import db, Invitation, Response,Result,Submission,Assessment

recruiter_bp = Blueprint('recruiter', __name__, url_prefix='/recruiter')

@recruiter_bp.route('/invite', methods=['POST'])
@jwt_required()
def send_invitation():
    data = request.get_json()
    if not data.get('interviewee_id') or not data.get('assessment_id'):
        return jsonify({'error':'interviewee_id and assessment_id required!'}),400
    invitation = Invitation(
        interviewee_id=data['interviewee_id'],
        assessment_id=data['assessment_id'],
        status='pending'
    )
    db.session.add(invitation)
    db.session.commit()
    return jsonify({'message': 'Invitation sent','invitation':invitation.serialize()}), 201

# @recruiter_bp.route('/invitations',methods=['GET'])
# @jwt_required()
# def get_invitations():
#     recruiter_id=get_jwt_identity()['id']
#     invitations=(Invitation.query.join(Assessment).filter(Assessment.recruiter_id==recruiter_id).all())
#     return jsonify([i.serialize() for i in invitation]),200

@recruiter_bp.route('/response', methods=['POST'])
@jwt_required()
def give_feedback():
    data = request.get_json()
    required=['question_id','submission_id','comment']
    if not all(field in data for field in required):
        return jsonify({'error':'question_id,submission_id and comment required!'}),400
    recruiter_id=get_jwt_identity()['id']
    response = Response(
        question_id=data['question_id'],
        submission_id=data['submission_id'],
        recruiter_id=recruiter_id,
        comment=data['comment']
    )
    db.session.add(response)
    db.session.commit()
    return jsonify({'message': 'Response submitted','response':response.serialize()}), 201

@recruiter_bp.route('/results', methods=['PATCH'])
@jwt_required()
def release_results():
    data = request.get_json()
    if not data.get('result_id'):
        return jsonify({'error':'result_id required!'}),400
    result = Result.query.get(data['result_id'])
    if not result:
        return jsonify({'error':'Result not found'}),404
        result.released = True
        db.session.commit()
        return jsonify({'message': 'Results released','result':result.serialize()}), 200
    


@recruiter_bp.route('/submissions/assessment/<int:assessment_id>',methods=['GET'])
@jwt_required()
def get_my_submissions(assessment_id):
    recruiter_id=get_jwt_identity()['id']
    assessment=Assessment.query.filter_by(id=assessment_id,recruiter_id=recruiter_id).first()
    if not assessment:
        return jsonify({'error':'Assessment Not Found!'}),404
    
    submissions=Submission.query.filter_by(assessment_id=assessment_id).all()
    return jsonify([s.serialize() for s in submissions]),200

@recruiter_bp.route('/submissions/<int:submission_id>',methods=['GET'])
@jwt_required()
def get_submission(submission_id):
    recruiter_id=get_jwt_identity()['id']
    submission=Submission.query.get(submission_id)
    if not submission:
        return jsonify({'error':'Submission not found!'}),404
    
    assessment=Assessment.query.filter_by(id=submission.assessment_id,recruiter_id=recruiter_id).first()
    if not assessment:
        return jsonify({'error':'Cannot Grant Access!'}),403
    return jsonify(submission.serialize()),200

