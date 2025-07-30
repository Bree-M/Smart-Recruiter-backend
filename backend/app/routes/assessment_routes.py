from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.app.models import db, Assessment

assessment_bp = Blueprint('assessments', __name__, url_prefix='/assessments')

@assessment_bp.route('/', methods=['POST'])
@jwt_required()
def create_assessment():
    user = get_jwt_identity()
    if user['role'] != 'recruiter':
        return jsonify({'error':'Only Recruiters Can Create Assessments!'}),403
    data=request.get_json()
    required_fields=['title','description','duration_minutes']
    if not all(field in data for field in required_fields):
        return jsonify({'error':'Title,Description and Durationn_minutes Required!'})
    
    assessment = Assessment(
        title=data['title'],
        description=data['description'],
        duration_minutes=data['duration_minutes'],
        recruiter_id=user['id']
    )
    db.session.add(assessment)
    db.session.commit()
    return jsonify({'message': 'Assessment created','assessment':assessment.serialize()}), 201

@assessment_bp.route('/', methods=['GET'])
@jwt_required()
def get_assessments():
    user=get_jwt_identity()
    query=Assessment.query
    if user['role'] == 'recruiter':
        query=query.filter_by(recruiter_id=user['id'])
    assessments = query.all()
    return jsonify([a.serialize() for a in assessments]), 200


@assessment_bp.route('/<int:id>',methods=['GET'])
@jwt_required()
def get_assessment(id):
    assessment=Assessment.query.get(id)
    if not assessment:
        return jsonify({'error':'Assessment ID not found!'}),404
    return jsonify(assessment.serialize()),200

@assessment_bp.route('/<int:id>',methods=['PATCH'])
@jwt_required()
def update_assessment(id):
    user=get_jwt_identity()
    assessment=Assessment.query.get(id)

    if not assessment:
        return jsonify({'error':'Assessment Not Found!'}),404
    
    if user['role'] != 'recrruiter' or assessment.recuiter_id != user['id']:
        return jsonify({'error':'Unauthorized!'}),403
    
    data=request.get_json()

    if 'title' in data:
        assessment.title=data['title']
    if 'description' in data:
        assessment.description=data['description']
    if 'duration-minutes' in data:
        assessment.minutes=data['duration_minutes']


    db.session.commit()    
    return jsonify({'message':'Assessment Updated.','assessment':assessment.serialize()}),200


@assessment_bp.route('/<int:id>',methods=['DELETE'])
@jwt_required()
def delete_assessment(id):
    user=get_jwt_identity()
    assessment=Assessment.query.get(id)
    if not assessment:
        return jsonify({'error':'Assessment not deleted!'}),404
    
    if user['role'] != 'recruiter' or assessment.recruiter_id != user['id']:
        return jsonify({'error':'Unauthorized To Delete Assessment!'}),403
    
    
    db.session.delete(assessment)
    db.session.commit()
    return jsonify({'message':'Assessment deleted'}),200


@assessment_bp.route('/recruiter/<int:recruiter_id>',methods=['GET'])
@jwt_required()
def get_assessment_by_recruiter(recruiter_id):
    assessments=Assessment.query.filter_by(recruiter_id=recruiter_id).all()
    return jsonify([a.serialize() for a in assessments]),200










