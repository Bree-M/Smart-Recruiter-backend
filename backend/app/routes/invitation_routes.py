from flask import Blueprint, request, jsonify
from backend.app.models import db, Invitation
from backend.app.models.user import User
from backend.app.models.assessment import Assessment
import traceback

invitation_bp = Blueprint('invitation', __name__, url_prefix='/invitations')

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


@invitation_bp.route('/', methods=['POST'])
def create_invitation():
    try:
        user = get_user_from_headers()
        if not user or user.role != 'recruiter':
            return jsonify({'error': 'Recruiter access required'}), 403

        data = request.get_json() or {}
        candidate_id = data.get('candidate_id')
        assessment_id = data.get('assessment_id')

        if not candidate_id or not assessment_id:
            return jsonify({'error': 'candidate_id and assessment_id are required'}), 400

        candidate = User.query.filter_by(id=candidate_id, role='candidate').first()
        assessment = Assessment.query.get(assessment_id)

        if not candidate:
            return jsonify({'error': 'Candidate not found or invalid'}), 404
        if not assessment or assessment.recruiter_id != user.id:
            return jsonify({'error': 'Assessment not found or unauthorized'}), 404

        existing_invite = Invitation.query.filter_by(
            recruiter_id=user.id,
            candidate_id=candidate_id,
            assessment_id=assessment_id
        ).first()
        if existing_invite:
            return jsonify({'error': 'Invitation already sent'}), 400

        invite = Invitation(
            recruiter_id=user.id,
            candidate_id=candidate_id,
            assessment_id=assessment_id,
            status='pending'
        )
        db.session.add(invite)
        db.session.commit()

        return jsonify({'message': 'Invitation sent', 'invitation': invite.serialize()}), 201

    except Exception as e:
        print(f"Exception in create_invitation: {e}")
        traceback.print_exc()
        return jsonify({'error': 'Internal server error'}), 500


@invitation_bp.route('/sent', methods=['GET'])
def list_sent_invitations():
    user = get_user_from_headers()
    if not user or user.role != 'recruiter':
        return jsonify({'error': 'Recruiter access required'}), 403

    invites = Invitation.query.filter_by(recruiter_id=user.id).order_by(Invitation.created_at.desc()).all()
    return jsonify([i.serialize() for i in invites]), 200


@invitation_bp.route('/received', methods=['GET'])
def list_received_invitations():
    user = get_user_from_headers()
    if not user or user.role != 'candidate':
        return jsonify({'error': 'Candidate access required'}), 403

    invites = Invitation.query.filter_by(candidate_id=user.id).order_by(Invitation.created_at.desc()).all()
    return jsonify([i.serialize() for i in invites]), 200


@invitation_bp.route('/<int:invitation_id>', methods=['PATCH'])
def update_invitation(invitation_id):
    user = get_user_from_headers()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401

    invite = Invitation.query.get(invitation_id)
    if not invite:
        return jsonify({'error': 'Invitation not found'}), 404

    if user.id not in [invite.candidate_id, invite.recruiter_id]:
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json() or {}
  
    if user.role == 'candidate' and 'status' in data:
        if data['status'] not in ['pending', 'accepted', 'declined']:
            return jsonify({'error': 'Invalid status value'}), 400
        invite.status = data['status']
        db.session.commit()
        return jsonify({'message': 'Invitation status updated', 'invitation': invite.serialize()}), 200

    if user.role == 'recruiter' and 'status' in data:
        if data['status'] not in ['pending', 'cancelled']:
            return jsonify({'error': 'Invalid status value'}), 400
        invite.status = data['status']
        db.session.commit()
        return jsonify({'message': 'Invitation updated', 'invitation': invite.serialize()}), 200

    return jsonify({'error': 'No valid fields to update or unauthorized action'}), 400


@invitation_bp.route('/<int:invitation_id>', methods=['DELETE'])
def delete_invitation(invitation_id):
    user = get_user_from_headers()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401

    invite = Invitation.query.get(invitation_id)
    if not invite:
        return jsonify({'error': 'Invitation not found'}), 404

    if user.id not in [invite.recruiter_id, invite.candidate_id]:
        return jsonify({'error': 'Unauthorized'}), 403

    db.session.delete(invite)
    db.session.commit()

    return jsonify({'message': 'Invitation deleted'}), 200
