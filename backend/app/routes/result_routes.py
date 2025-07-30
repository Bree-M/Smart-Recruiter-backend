from flask import Blueprint,request,jsonify
from flask_jwt_extended import jwt_required,get_jwt_identity
from backend.app.models import db,Result,Submission

result_bp=Blueprint('results',__name__,url_prefix='/results')
@result_bp.route('/<int:submission_id>',methods=['GET'])
@jwt_required()
def get_result(submission_id):
    user=get_jwt_identity()
    submission=Submission.query.filter_by(id=submission_id,interviewee_id=user['id']).first()
    if not submission:
        return jsonify({'error':'Submission Not Found!'}),404
    
    if user['role']=='interviewee' and submission.interviewee_id != user['id']:
        return jsonify({'error':'Authorization Request!'}),403
    if not submission.result:
        return jsonify({'error':'Result Not Found!'}),404
    if user['role'] == 'interviewee' and not submission.result.released:
        return jsonify({'error':'Result Not Out!'}),403
    
    return jsonify(submission.result.serialize()),200

@result_bp.route('/',methods=['GET'])
@jwt_required()
def get_all_results():
    user=get_jwt_identity()
    if user['role'] != 'recruiter':
        return jsonify({'error':'Only Recruiters Can View All Results!'}),403
    results=Result.query.join(Submission).join(Submission.assessment).filter_by(recruiter_id=user['id']).all()
    return jsonify([r.serialize() for r in results]),200




@result_bp.route('/<int:submission_id>',methods=['POST','PATCH'])
@jwt_required()
def create_or_update_result(submission_id):
    user=get_jwt_identity()
    if user['role'] != 'recruiter':
        return jsonify({'error':'Only Recruiters Can Grade!'}),403
    submission=Submission.query.get(submission_id)
    if not submission:
        return jsonify({'error':'Submission Not Found!'}),404
    if submission.assessment.recruiter_id != user['id']:
        return jsonify({'error':'Authorization Required!'}),403
    
    data=request.get_json()
    required_fields=['total_score','max_score','grade']
    if not all(field in data for field in required_fields):
        return jsonify({'error':'Fields Required!'}),400

    result=Result.query.filter_by(submission_id=submission_id).first()
    if result:
        result.total_score=data['total_score']
        result.max_score=data['max_score']
        result.grade=data['grade']
        result.feedback_summary=data.get('feedback_summary',result.feedback_summary)
        message='Result Updated'
    else:
        result=Result(
            submission_id=submission_id,
            total_score=data['total_score'],
            max_score=data['max_score'],
            grade=data['grade'],
            feedback_summary=data.get('feedback_summary')
        )    
        db.session.add(result)
        message='Result Created'

    db.session.commit()
    return jsonify({'message':'Result Created','result':result.serialize()}),200
    
@result_bp.route('/released/<int:result_id>',methods=['PATCH'])
@jwt_required()
def released_result(result_id):
    user=get_jwt_identity()
    if user['role'] != 'recruiter':
        return jsonify({'error':'Only Recruiters Can Release Results!'}),403
    result=Result.query.get(result_id)
    if not result:
        return jsonify({'error':'Result Not Found!'}),404
    if result.submission.assessment.recruiter_id != user['id']:
        return jsonify({'error':'Authorization Required!'}),403
    result.released=True
    db.session.commit()
    return jsonify({'message':'Result Released Successfully.','result':result.serialize()}),200


@result_bp.route('/<int:result_id>',methods=['DELETE'])
@jwt_required()
def delete_result(result_id):
    user=get_jwt_identity()
    if user['role'] != 'recruiter':
        return jsonify({'error':'Only Recruiters Can Delete Result'}),403
    result=Result.query.get(result_id)
    if not result:
        return jsonify({'error':'Result Not Found!'}),404
    if result.submission.assessment.recruiter_id != user['id']:
        return jsonify({'error':'Authorization Required!'}),403
    
    db.session.delete(result)
    db.session.commit()
    return jsonify({'message':'Result Deleted.'}),200
    



