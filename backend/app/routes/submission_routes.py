from flask import Blueprint, request, jsonify
from backend.app.models import db, Submission, Response
from backend.app.models.user import User
from backend.app.models.assessment import Assessment
from backend.app.models.question import Question

submission_bp = Blueprint('submission', __name__, url_prefix='/submissions')

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

@submission_bp.route('/', methods=['POST'])
def create_submission():
    user = get_user_from_headers()
    if not user or user.role != 'candidate':
        return jsonify({'error': 'Candidate access required'}), 403

    data = request.get_json() or {}
    assessment_id = data.get('assessment_id')
    answers = data.get('answers')  

    if not assessment_id or not answers:
        return jsonify({'error': 'assessment_id and answers are required'}), 400

    assessment = Assessment.query.get(assessment_id)
    if not assessment:
        return jsonify({'error': 'Assessment not found'}), 404


    submission = Submission(candidate_id=user.id, assessment_id=assessment_id, status='submitted')
    db.session.add(submission)
    db.session.flush()

    for q_id_str, answer_text in answers.items():
        try:
            q_id = int(q_id_str)
        except ValueError:
            continue
        question = Question.query.get(q_id)
        if question and question.assessment_id == assessment_id:
            response = Response(submission_id=submission.id, question_id=q_id, answer_text=answer_text)
            db.session.add(response)

    db.session.commit()
    return jsonify({'message': 'Submission created', 'submission': submission.serialize()}), 201

@submission_bp.route('/candidate', methods=['GET'])
def list_candidate_submissions():
    user = get_user_from_headers()
    if not user or user.role != 'candidate':
        return jsonify({'error': 'Candidate access required'}), 403

    submissions = Submission.query.filter_by(candidate_id=user.id).order_by(Submission.submitted_at.desc()).all()
    return jsonify([s.serialize() for s in submissions]), 200


@submission_bp.route('/<int:submission_id>', methods=['GET'])
def get_submission(submission_id):
    user = get_user_from_headers()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401

    submission = Submission.query.get(submission_id)
    if not submission:
        return jsonify({'error': 'Submission not found'}), 404

   
    if user.role == 'candidate' and submission.candidate_id != user.id:
        return jsonify({'error': 'Unauthorized'}), 403

   
    if user.role == 'recruiter' and submission.assessment.recruiter_id != user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    return jsonify(submission.serialize()), 200


@submission_bp.route('/<int:submission_id>', methods=['PATCH'])
def update_submission(submission_id):
    user = get_user_from_headers()
    if not user or user.role != 'candidate':
        return jsonify({'error': 'Candidate access required'}), 403

    submission = Submission.query.get(submission_id)
    if not submission:
        return jsonify({'error': 'Submission not found'}), 404
    if submission.candidate_id != user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json() or {}
    answers = data.get('answers') 

    if answers:
    
        Response.query.filter_by(submission_id=submission.id).delete()
        for q_id_str, answer_text in answers.items():
            try:
                q_id = int(q_id_str)
            except ValueError:
                continue
            question = Question.query.get(q_id)
            if question and question.assessment_id == submission.assessment_id:
                response = Response(submission_id=submission.id, question_id=q_id, answer_text=answer_text)
                db.session.add(response)

    db.session.commit()
    return jsonify({'message': 'Submission updated', 'submission': submission.serialize()}), 200


@submission_bp.route('/<int:submission_id>', methods=['DELETE'])
def delete_submission(submission_id):
    user = get_user_from_headers()
    if not user or user.role != 'candidate':
        return jsonify({'error': 'Candidate access required'}), 403

    submission = Submission.query.get(submission_id)
    if not submission:
        return jsonify({'error': 'Submission not found'}), 404
    if submission.candidate_id != user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    db.session.delete(submission)
    db.session.commit()
    return jsonify({'message': 'Submission deleted'}), 200


@submission_bp.route('/assessment/<int:assessment_id>', methods=['GET'])
def list_submissions_for_assessment(assessment_id):
    user = get_user_from_headers()
    if not user or user.role != 'recruiter':
        return jsonify({'error': 'Recruiter access required'}), 403

    submissions = Submission.query.filter_by(assessment_id=assessment_id).all()
  
    submissions = [s for s in submissions if s.assessment.recruiter_id == user.id]
    return jsonify([s.serialize() for s in submissions]), 200

@submission_bp.route('/<int:submission_id>/grade', methods=['PATCH'])
def grade_submission(submission_id):
    user = get_user_from_headers()
    if not user or user.role != 'recruiter':
        return jsonify({'error': 'Recruiter access required'}), 403

    submission = Submission.query.get(submission_id)
    if not submission:
        return jsonify({'error': 'Submission not found'}), 404
    if submission.assessment.recruiter_id != user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json() or {}
    score = data.get('score')
    status = data.get('status')

    if score is not None:
        try:
            submission.score = float(score)
        except ValueError:
            return jsonify({'error': 'Invalid score value'}), 400
    if status:
        if status not in ['submitted', 'graded', 'reviewed']:
            return jsonify({'error': 'Invalid status value'}), 400
        submission.status = status

    db.session.commit()
    return jsonify({'message': 'Submission graded', 'submission': submission.serialize()}), 200

@submission_bp.route('/<int:submission_id>/delete', methods=['DELETE'])
def delete_submission_recruiter(submission_id):
    user = get_user_from_headers()
    if not user or user.role != 'recruiter':
        return jsonify({'error': 'Recruiter access required'}), 403

    submission = Submission.query.get(submission_id)
    if not submission:
        return jsonify({'error': 'Submission not found'}), 404
    if submission.assessment.recruiter_id != user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    db.session.delete(submission)
    db.session.commit()
    return jsonify({'message': 'Submission deleted'}), 200
