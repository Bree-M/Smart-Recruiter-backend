from flask import Blueprint, request, jsonify, current_app
from backend.app.models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

def get_current_user():
    token = request.headers.get('Authorization')
    if not token:
        return None
    try:
        data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return User.query.get(data['user_id'])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = get_current_user()
        if not user:
            return jsonify({'error': 'Unauthorized'}), 401
        request.user = user
        return f(*args, **kwargs)
    return decorated

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    required_fields = ['username', 'email', 'password', 'role']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    if User.query.filter((User.username == data['username']) | (User.email == data['email'])).first():
        return jsonify({'error': 'User already exists'}), 400

    user = User(
        username=data['username'],
        email=data['email'],
        role=data['role'],
        phone_number=data.get('phone_number')
    )
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully', 'user_id': user.id}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data.get('email')).first()

    if not user or not user.check_password(data.get('password')):
        return jsonify({'error': 'Invalid email or password'}), 401

    token = jwt.encode({
        'user_id': user.id,
        'role': user.role,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=current_app.config.get('JWT_EXPIRATION_HOURS', 24))
    }, current_app.config['SECRET_KEY'], algorithm='HS256')

    return jsonify({
        'message': 'Login successful',
        'role': user.role,
        'user_id': user.id,
        'token': token
    })

@auth_bp.route('/me', methods=['GET'])
@token_required
def me():
    user = request.user
    return jsonify(user.serialize()), 200

@auth_bp.route('/logout', methods=['POST'])
@token_required
def logout():
    return jsonify({'message': 'User logged out successfully'}), 200
