from flask import Blueprint, request, jsonify
from backend.app.models import db, Feedback, Submission
from backend.app.models.user import User

feedback_bp = Blueprint('feedback', __name__, url_prefix='/feedbacks')

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

@feedback_bp.route('/', methods=['POST'])
def create_feedback():
    user = get_user_from_headers()
    if not user or user.role != 'recruiter':
        return jsonify({"error": "Recruiter access required"}), 403

    data = request.get_json() or {}
    submission_id = data.get('submission_id')
    comment = data.get('comment')

    if not submission_id or not comment:
        return jsonify({"error": "submission_id and comment are required"}), 400

    submission = Submission.query.get(submission_id)
    if not submission:
        return jsonify({"error": "Submission not found"}), 404

    if submission.assessment.recruiter_id != user.id:
        return jsonify({"error": "Unauthorized"}), 403

    feedback = Feedback(
        submission_id=submission_id,
        recruiter_id=user.id,
        comment=comment
    )
    db.session.add(feedback)
    db.session.commit()

    return jsonify({"message": "Feedback created", "feedback": feedback.serialize()}), 201

@feedback_bp.route('/<int:feedback_id>', methods=['GET'])
def get_feedback(feedback_id):
    feedback = Feedback.query.get(feedback_id)
    if not feedback:
        return jsonify({"error": "Feedback not found"}), 404
    return jsonify(feedback.serialize()), 200

@feedback_bp.route('/submission/<int:submission_id>', methods=['GET'])
def get_feedbacks_for_submission(submission_id):
    feedbacks = Feedback.query.filter_by(submission_id=submission_id).all()
    return jsonify([f.serialize() for f in feedbacks]), 200

@feedback_bp.route('/<int:feedback_id>', methods=['PATCH'])
def update_feedback(feedback_id):
    user = get_user_from_headers()
    if not user or user.role != 'recruiter':
        return jsonify({"error": "Recruiter access required"}), 403

    feedback = Feedback.query.get(feedback_id)
    if not feedback:
        return jsonify({"error": "Feedback not found"}), 404

    if feedback.recruiter_id != user.id:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json() or {}
    if 'comment' in data:
        feedback.comment = data['comment']

    db.session.commit()
    return jsonify({"message": "Feedback updated", "feedback": feedback.serialize()}), 200

@feedback_bp.route('/<int:feedback_id>', methods=['DELETE'])
def delete_feedback(feedback_id):
    user = get_user_from_headers()
    if not user or user.role != 'recruiter':
        return jsonify({"error": "Recruiter access required"}), 403

    feedback = Feedback.query.get(feedback_id)
    if not feedback:
        return jsonify({"error": "Feedback not found"}), 404

    if feedback.recruiter_id != user.id:
        return jsonify({"error": "Unauthorized"}), 403

    db.session.delete(feedback)
    db.session.commit()
    return jsonify({"message": "Feedback deleted"}), 200
