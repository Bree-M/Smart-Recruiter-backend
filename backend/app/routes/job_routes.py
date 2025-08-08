from flask import Blueprint, request, jsonify
from backend.app.models import db, Job
from backend.app.models.user import User

jobs_bp = Blueprint('jobs', __name__, url_prefix='/jobs')

# Helper to get user info from headers (same as auth)
def get_user_from_headers():
    user_id = request.headers.get('User-ID')
    role = request.headers.get('User-Role')
    if not user_id or not role:
        return None
    user = User.query.get(user_id)
    if not user or user.role != role:
        return None
    return user

@jobs_bp.route('/', methods=['POST'])
def create_job():
    user = get_user_from_headers()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401
    if user.role != 'recruiter':
        return jsonify({"error": "Only recruiters can create jobs"}), 403

    data = request.get_json() or {}
    if not data.get('title') or not data.get('description'):
        return jsonify({"error": "title and description are required"}), 400

    job = Job(
        title=data['title'],
        description=data['description'],
        location=data.get('location'),
        employment_type=data.get('employment_type'),
        salary_range=data.get('salary_range'),
        is_active=data.get('is_active', True),
        recruiter_id=user.id
    )
    db.session.add(job)
    db.session.commit()

    return jsonify({"message": "Job created", "job": job.serialize()}), 201


@jobs_bp.route('/', methods=['GET'])
def list_jobs_public():
    jobs = Job.query.filter_by(is_active=True).order_by(Job.created_at.desc()).all()
    return jsonify([j.serialize() for j in jobs]), 200


@jobs_bp.route('/mine', methods=['GET'])
def list_my_jobs():
    user = get_user_from_headers()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401
    if user.role != 'recruiter':
        return jsonify({"error": "Recruiter access required"}), 403

    jobs = Job.query.filter_by(recruiter_id=user.id).order_by(Job.created_at.desc()).all()
    return jsonify([j.serialize() for j in jobs]), 200


@jobs_bp.route('/<int:job_id>', methods=['GET'])
def get_job(job_id):
    job = Job.query.get(job_id)
    if not job:
        return jsonify({"error": "Job not found"}), 404

    if job.is_active:
        return jsonify(job.serialize()), 200

    # Job inactive - only recruiter owner can see
    user = get_user_from_headers()
    if user and user.role == 'recruiter' and user.id == job.recruiter_id:
        return jsonify(job.serialize()), 200

    return jsonify({"error": "Job not available"}), 403


@jobs_bp.route('/<int:job_id>', methods=['PATCH'])
def update_job(job_id):
    user = get_user_from_headers()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401
    if user.role != 'recruiter':
        return jsonify({"error": "Recruiter access required"}), 403

    job = Job.query.get(job_id)
    if not job:
        return jsonify({"error": "Job not found"}), 404
    if job.recruiter_id != user.id:
        return jsonify({"error": "Unauthorized to modify this job"}), 403

    data = request.get_json() or {}
    if 'title' in data:
        job.title = data['title']
    if 'description' in data:
        job.description = data['description']
    if 'location' in data:
        job.location = data['location']
    if 'employment_type' in data:
        job.employment_type = data['employment_type']
    if 'salary_range' in data:
        job.salary_range = data['salary_range']
    if 'is_active' in data:
        job.is_active = bool(data['is_active'])

    db.session.commit()
    return jsonify({"message": "Job updated", "job": job.serialize()}), 200


@jobs_bp.route('/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    user = get_user_from_headers()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401
    if user.role != 'recruiter':
        return jsonify({"error": "Recruiter access required"}), 403

    job = Job.query.get(job_id)
    if not job:
        return jsonify({"error": "Job not found"}), 404
    if job.recruiter_id != user.id:
        return jsonify({"error": "Unauthorized to delete this job"}), 403

    db.session.delete(job)
    db.session.commit()
    return jsonify({"message": "Job deleted"}), 200
