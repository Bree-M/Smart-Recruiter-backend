from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity,create_refresh_token
from backend.app.models import db, User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    required_fields=['username','email','password','roe']
    if not all(field in data for field in required_fields):
        return jsonify({'error':'Username,Email,Password And Role Required!'}),404
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error':'Email already exists'}),409
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error':'Username aleady taken!'}),409
    
    if data['role'] not in ['recruiter','candidate']:
        return jsonify({'error':'Role Must Be Either Recruiter Or Candidate!'}),400

    user = User(
        username=data['username'],
        email=data['email'],
        profile_picture_url=data.get('profile_picture_url'),
        bio=data.get('bio'),
        about_me=data.get('about_me'),
        company_name=data.get('company_name'),
        skills=data.get('skills'),
        role=data['role']
    )

    user.set_password(data['password'])

    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered','user':user.serialize()}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not all(field in data for field in ['email','password']):
        return jsonify ({'error':'Email And Password required!'})
    user = User.query.filter_by(email=data['email']).first()
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid Entries!'}),401
                        
    access_token=create_access_token(identity={'id':user.id,'role':user.role})
    refresh_token=create_refresh_token(identity={'id':user.id,'role':user.role})
    
    return jsonify({'message':'Login Successful!','access_token':access_token,'refresh_token':refresh_token,'user':user.serialize()}),200

@auth_bp.route('/logout',methods=['POST'])
@jwt_required()
def log_out():
    return jsonify({'message':'Successfully Logged Out!'}),200


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    return jsonify(get_jwt_identity()), 200
