from flask import Blueprint, request, jsonify
from backend.app.models import db, Result, Submission
from backend.app.models.user import User

result_bp = Blueprint('result', __name__, url_prefix='/results')

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

@result_bp.route('/', methods=['POST'])
def create_result():
    user = get_user_from_headers()
    if not user or user.role != 'recruiter':
        return jsonify({"error": "Recruiter access required"}), 403

    data = request.get_json() or {}
    submission_id = data.get('submission_id')
    score = data.get('score')
    feedback_text = data.get('feedback', '')

    if not submission_id or score is None:
        return jsonify({"error": "submission_id and score are required"}), 400

    submission = Submission.query.get(submission_id)
    if not submission:
        return jsonify({"error": "Submission not found"}), 404

 
    if submission.assessment.recruiter_id != user.id:
        return jsonify({"error": "Unauthorized"}), 403

    existing_result = Result.query.filter_by(submission_id=submission_id).first()
    if existing_result:
        return jsonify({"error": "Result already exists for this submission"}), 400

    result = Result(
        submission_id=submission_id,
        candidate_id=submission.candidate_id,
        assessment_id=submission.assessment_id,
        score=score,
        feedback=feedback_text
    )
    db.session.add(result)
    db.session.commit()

    return jsonify({"message": "Result created", "result": result.serialize()}), 201

@result_bp.route('/<int:result_id>', methods=['GET'])
def get_result(result_id):
    result = Result.query.get(result_id)
    if not result:
        return jsonify({"error": "Result not found"}), 404
    return jsonify(result.serialize()), 200

@result_bp.route('/submission/<int:submission_id>', methods=['GET'])
def get_result_by_submission(submission_id):
    result = Result.query.filter_by(submission_id=submission_id).first()
    if not result:
        return jsonify({"error": "Result not found for submission"}), 404
    return jsonify(result.serialize()), 200

@result_bp.route('/<int:result_id>', methods=['PATCH'])
def update_result(result_id):
    user = get_user_from_headers()
    if not user or user.role != 'recruiter':
        return jsonify({"error": "Recruiter access required"}), 403

    result = Result.query.get(result_id)
    if not result:
        return jsonify({"error": "Result not found"}), 404

    if result.assessment.recruiter_id != user.id:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json() or {}
    if 'score' in data:
        result.score = data['score']
    if 'feedback' in data:
        result.feedback = data['feedback']

    db.session.commit()
    return jsonify({"message": "Result updated", "result": result.serialize()}), 200

@result_bp.route('/<int:result_id>', methods=['DELETE'])
def delete_result(result_id):
    user = get_user_from_headers()
    if not user or user.role != 'recruiter':
        return jsonify({"error": "Recruiter access required"}), 403

    result = Result.query.get(result_id)
    if not result:
        return jsonify({"error": "Result not found"}), 404

    if result.assessment.recruiter_id != user.id:
        return jsonify({"error": "Unauthorized"}), 403

    db.session.delete(result)
    db.session.commit()
    return jsonify({"message": "Result deleted"}), 200
