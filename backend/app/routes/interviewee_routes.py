from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

interviewee_bp = Blueprint('interviewee', __name__, url_prefix='/interviewee')

@interviewee_bp.route('/jobs', methods=['GET'])
@jwt_required()
def interviewee_jobs():
    identity = get_jwt_identity()
    # Placeholder response - show active jobs for interviewee
    return jsonify({
        "message": "Available jobs for interviewee",
        "user_id": identity.get('user_id'),
        "role": identity.get('role')
    })

@interviewee_bp.route('/submissions', methods=['GET'])
@jwt_required()
def submissions():
    identity = get_jwt_identity()
    # Placeholder response - user's submissions
    return jsonify({
        "message": "List of user's submissions",
        "user_id": identity.get('user_id')
    })

@interviewee_bp.route('/submit-assessment', methods=['POST'])
@jwt_required()
def submit_assessment():
    identity = get_jwt_identity()
    data = request.json
    # For now, echo what was received
    return jsonify({
        "message": "Assessment submitted",
        "user_id": identity.get('user_id'),
        "data_received": data
    })
