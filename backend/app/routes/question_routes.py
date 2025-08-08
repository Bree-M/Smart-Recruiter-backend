from flask import Blueprint, request, jsonify
from backend.app.models import db, Question, Assessment
from backend.app.models.user import User

question_bp = Blueprint('question', __name__, url_prefix='/questions')

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

@question_bp.route('/', methods=['POST'])
def create_question():
    user = get_user_from_headers()
    if not user or user.role != 'recruiter':
        return jsonify({'error': 'Recruiter access required'}), 403

    data = request.get_json() or {}
    assessment_id = data.get('assessment_id')
    question_text = data.get('question_text')
    question_type = data.get('question_type')
    choices = data.get('choices') 
    correct_answer = data.get('correct_answer')
    points = data.get('points', 1)

    if not assessment_id or not question_text or not question_type:
        return jsonify({'error': 'assessment_id, question_text, and question_type are required'}), 400

    assessment = Assessment.query.get(assessment_id)
    if not assessment or assessment.recruiter_id != user.id:
        return jsonify({'error': 'Assessment not found or unauthorized'}), 404

    if question_type == 'multiple_choice' and not choices:
        return jsonify({'error': 'Choices are required for multiple choice questions'}), 400

    question = Question(
        assessment_id=assessment_id,
        question_text=question_text,
        question_type=question_type,
        choices=choices,
        correct_answer=correct_answer,
        points=points
    )
    db.session.add(question)
    db.session.commit()

    return jsonify({'message': 'Question created', 'question': question.serialize()}), 201


@question_bp.route('/<int:question_id>', methods=['GET'])
def get_question(question_id):
    question = Question.query.get(question_id)
    if not question:
        return jsonify({'error': 'Question not found'}), 404
    return jsonify(question.serialize()), 200


@question_bp.route('/assessment/<int:assessment_id>', methods=['GET'])
def list_questions_for_assessment(assessment_id):
    questions = Question.query.filter_by(assessment_id=assessment_id).all()
    return jsonify([q.serialize() for q in questions]), 200


@question_bp.route('/<int:question_id>', methods=['PATCH'])
def update_question(question_id):
    user = get_user_from_headers()
    if not user or user.role != 'recruiter':
        return jsonify({'error': 'Recruiter access required'}), 403

    question = Question.query.get(question_id)
    if not question:
        return jsonify({'error': 'Question not found'}), 404

    if question.assessment.recruiter_id != user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json() or {}

    for field in ['question_text', 'question_type', 'choices', 'correct_answer', 'points']:
        if field in data:
            setattr(question, field, data[field])

    db.session.commit()
    return jsonify({'message': 'Question updated', 'question': question.serialize()}), 200


@question_bp.route('/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    user = get_user_from_headers()
    if not user or user.role != 'recruiter':
        return jsonify({'error': 'Recruiter access required'}), 403

    question = Question.query.get(question_id)
    if not question:
        return jsonify({'error': 'Question not found'}), 404

    if question.assessment.recruiter_id != user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    db.session.delete(question)
    db.session.commit()
    return jsonify({'message': 'Question deleted'}), 200
