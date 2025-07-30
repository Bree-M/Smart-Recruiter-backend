from flask import Blueprint,request,jsonify
from flask_jwt_extended import jwt_required,get_jwt_identity
from backend.app.models import db,Question,Assessment

question_bp=Blueprint('questions',__name__,url_prefix='/questions')

@question_bp.route('/',methods=['POST'])
@jwt_required()
def create_question():
    user=get_jwt_identity()
    if user['role'] != 'recruiter':
        return jsonify({'error':'Only Recruiters Can Create Questions!'}),403
    
    data=request.get_json()
    required=['assessment_id','text']
    if not all(k in data for k in required):
        return jsonify({'error':'Fields Required!'}),400
    assessment=Assessment.query.filter_by(id=data['assessment_id'],recruiter_id=user['id']).first()
    if not assessment:
        return jsonify({'error':'Assessment Not Found!'}),404
    
    question=Question(
        assessment_id=data['assessment_id'],
        text=data['text'],
        type=data.get('type','text'),
        options=data.get('options'),
        correct_answer=data.get('correct_answer')


    )
    db.session.add(question)
    db.session.commit()
    return jsonify({'message':'Question Created.','question':question.serialize()}),201

@question_bp.route('/<int:question_id>',methods=['PATCH'])
@jwt_required()
def update_question(question_id):
    user=get_jwt_identity()
    if user['role'] != 'recruiter':
        return jsonify({'error':'Only Recruiters Can Make Updates!'}),403
    
    question=Question.query.get(question_id)
    if not question:
        return jsonify({'error':'Question Not Found!'}),404
    if question.assessment.recruiter_id != user['id']:
        return jsonify({'error':'Authorization Required!'}),403
    
    data=request.get_json()
    if 'text' in data:
        question.text=data['text']
    if 'type' in data:
        question.type=data['type']    
    if 'options' in data:
        question.options=data['options']    
    if 'correct_answer' in data:
        question.correct_answer=data['correct_answer']    

    db.session.commit()    
    return jsonify({'message':'Question Updated','question':question.serialize()}),200


@question_bp.route('/<int:question_id>',methods=['DELETE'])
@jwt_required()
def delete_question(question_id):
    user=get_jwt_identity()
    if user['role'] != 'recruiter':
        return jsonify({'error':'Only Recruiter Can Delete Question!'}),403
    
    question=Question.query.get(question_id)
    if not question:
        return jsonify({'error':'Question Not Found!'}),404
    if question.assessment.recruiter_id != user['id']:
        return jsonify({'error':'Authorization Required!'}),403
    
    db.session.delete(question)
    db.session.commit()
    return jsonify({'message':'Question Deleted'}),200


@question_bp.route('/assessment/<int:assessment_id>',methods=['GET'])
@jwt_required()
def get_questions(assessment_id):
    questions=Question.query.filter_by(assessment_id=assessment_id).all()
    if not questions:
        return jsonify({'error':'Question Not Found'}),404
    return jsonify([q.serialize() for q in questions]),200





    



    