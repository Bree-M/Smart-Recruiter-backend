from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from backend.app import db
from backend.app.models.user import User
from functools import wraps
import jwt
import datetime
from flask import current_app

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

def get_current_user():
    token = request.headers.get('Authorization')
    if not token:
        return None
    try:
        data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return db.session.get(User, data['user_id'])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None



def recruiter_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        if not user or user.role != 'recruiter':
            return jsonify({'error': 'Recruiter access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

def candidate_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        if not user or user.role != 'candidate':
            return jsonify({'error': 'Candidate access required'}), 403
        return f(*args, **kwargs)
    return decorated_function


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
    if not data or not data.get('username') or not data.get('email') or not data.get('password') or not data.get('role'):
        return jsonify({'error': 'Missing required fields'}), 400

    if User.query.filter((User.username == data['username']) | (User.email == data['email'])).first():
        return jsonify({'error': 'User already exists'}), 400

    hashed_password = generate_password_hash(data['password'])
    user = User(
        username=data['username'],
        email=data['email'],
        password_hash=hashed_password,
        role=data['role']
    )
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully', 'user_id': user.id}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()

    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid email or password'}), 401

    token = jwt.encode({
        'user_id': user.id,
        'role': user.role,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=current_app.config['JWT_EXPIRATION_HOURS'])
    }, current_app.config['SECRET_KEY'], algorithm='HS256')

    return jsonify({
        'message': 'Login successful',
        'role': user.role,
        'user_id': user.id,
        'token': token
    })


@auth_bp.route('/logout', methods=['POST'])
def logout():
    return jsonify({'message': 'User logged out successfully'}), 200


@auth_bp.route('/me', methods=['GET'])
def me():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401
    return jsonify(user.to_dict()), 200

@auth_bp.route('/dashboard', methods=['GET'])
def dashboard():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401

    if user.role == 'recruiter':
        return jsonify({'message': 'Welcome to the Recruiter dashboard'}), 200
    elif user.role == 'candidate':
        return jsonify({'message': 'Welcome to the Candidate dashboard'}), 200
    else:
        return jsonify({'error': 'Invalid role'}), 400

@auth_bp.route('/recruiter-area', methods=['GET'])
@recruiter_required
def recruiter_area():
    return jsonify({'message': 'This is the recruiter-only area'}), 200

@auth_bp.route('/candidate-area', methods=['GET'])
@candidate_required
def candidate_area():
    return jsonify({'message': 'This is the candidate-only area'}), 200
