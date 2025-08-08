from flask import Blueprint, request, jsonify
from backend.app.models import db, Assessment
from backend.app.models.user import User

assessment_bp = Blueprint('assessment', __name__, url_prefix='/assessments')

def get_user_from_headers():
    user_id = request.headers.get('User-ID')
    user_role = request.headers.get('User-Role')
    if not user_id or not user_role:
        return None
    try:
        user = User.query.get(int(user_id))
    except Exception:
        return None
    if user and user.role == user_role:
        return user
    return None


@assessment_bp.route('/', methods=['POST'])
def create_assessment():
    user = get_user_from_headers()
    if not user or user.role != 'recruiter':
        return jsonify({'error': 'Recruiter access required'}), 403

    data = request.get_json() or {}
    title = data.get('title')
    description = data.get('description')
    if not title or not description:
        return jsonify({'error': 'Title and description are required'}), 400

    assessment = Assessment(
        title=title,
        description=description,
        time_limit=data.get('time_limit'),
        difficulty=data.get('difficulty'),
        is_published=data.get('is_published', False),
        category=data.get('category'),
        recruiter_id=user.id
    )
    db.session.add(assessment)
    db.session.commit()

    return jsonify({'message': 'Assessment created', 'assessment': assessment.serialize()}), 201


@assessment_bp.route('/', methods=['GET'])
def list_assessments():
    assessments = Assessment.query.order_by(Assessment.created_at.desc()).all()
    return jsonify([a.serialize() for a in assessments]), 200


@assessment_bp.route('/<int:assessment_id>', methods=['GET'])
def get_assessment(assessment_id):
    assessment = Assessment.query.get(assessment_id)
    if not assessment:
        return jsonify({'error': 'Assessment not found'}), 404
    return jsonify(assessment.serialize()), 200


@assessment_bp.route('/<int:assessment_id>', methods=['PATCH'])
def update_assessment(assessment_id):
    user = get_user_from_headers()
    if not user or user.role != 'recruiter':
        return jsonify({'error': 'Recruiter access required'}), 403

    assessment = Assessment.query.get(assessment_id)
    if not assessment:
        return jsonify({'error': 'Assessment not found'}), 404
    if assessment.recruiter_id != user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json() or {}
    for field in ['title', 'description', 'time_limit', 'difficulty', 'is_published', 'category']:
        if field in data:
            setattr(assessment, field, data[field])

    db.session.commit()
    return jsonify({'message': 'Assessment updated', 'assessment': assessment.serialize()}), 200


@assessment_bp.route('/<int:assessment_id>', methods=['DELETE'])
def delete_assessment(assessment_id):
    user = get_user_from_headers()
    if not user or user.role != 'recruiter':
        return jsonify({'error': 'Recruiter access required'}), 403

    assessment = Assessment.query.get(assessment_id)
    if not assessment:
        return jsonify({'error': 'Assessment not found'}), 404
    if assessment.recruiter_id != user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    db.session.delete(assessment)
    db.session.commit()
    return jsonify({'message': 'Assessment deleted'}), 200
