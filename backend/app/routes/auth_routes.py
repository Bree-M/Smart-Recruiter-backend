from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from backend.app.models import db, User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
   
    if not data or not all(k in data for k in ['username','email','password','role']):
        return jsonify({'error':'Field required'})
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error':'Email already exists'}),409
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error':'Username aleady taken!'}),409

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
    return jsonify({'message': 'User registered'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not all(k in data for k in ['email','password']):
        return jsonify ({'error':'Field required!'})
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        return jsonify({'error': 'User not found!'}),404
                        
    if not user.check_password(data['password']):
        return jsonify({'error':'Invalid entry'}),401
    
    token = create_access_token(identity={'id': user.id, 'role': user.role})
    return jsonify({'access_token': token}), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    return jsonify(get_jwt_identity()), 200
