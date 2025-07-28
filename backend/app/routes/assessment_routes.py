from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.app.models import db, Assessment

assessment_bp = Blueprint('assessments', __name__, url_prefix='/assessments')

@assessment_bp.route('/', methods=['POST'])
@jwt_required()
def create_assessment():
    data = request.get_json()
    user = get_jwt_identity()
    assessment = Assessment(
        title=data['title'],
        description=data['description'],
        duration_minutes=data['duration_minutes'],
        recruiter_id=user['id']
    )
    db.session.add(assessment)
    db.session.commit()
    return jsonify({'message': 'Assessment created'}), 201

@assessment_bp.route('/', methods=['GET'])
@jwt_required()
def get_assessments():
    assessments = Assessment.query.all()
    return jsonify([a.serialize() for a in assessments]), 200


@assessment_bp.route('/<int:id>',methods=['GET'])
@jwt_required()
def get_password(id):
    assessment=Assessment.query.get(id)
    if not assessment:
        return jsonify({'error':'Assessment ID not found!'}),404
    return jsonify(assessment.serialie()),200

@assessment_bp.route('/<int:id>',methods=['PATCH'])
@jwt_required()
def update_assessment(id):
    data=request.get_json()
    assessment=Assessment.query.get(id)

    if not assessment:
        return jsonify({'error':'Assessment Update Not Found!'}),404
    if 'title' in data:
        assessment.title=data['title']
    if 'description' in data:
        assessment.description=data['description']
    if 'duration-minutes' in data:
        assessment.minutes=data['dutation-minutes']


    db.session.commit()    
    return jsonify({'message':'Assessment Updated.'}),202


# @assessment_bp.route('/<int:id>',methods=['DELETE'])
# @jwt_required()
# def delete_assessment(id):
#     assessment=Assessment.query.get(id)
#     if not assessment:
#         return jsonify({'error':'Assessment not deleted!'}),404
    
#     db.session.delete(assessment)
#     db.session.commit()
#     return jsonify({'message':'Assessment deleted'}),202









