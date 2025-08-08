from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    load_dotenv()
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('backend.app.config.Config')  

   
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', app.config['SQLALCHEMY_DATABASE_URI'])
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', app.config['JWT_SECRET_KEY'])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    print(f"JWT_SECRET_KEY used: {app.config['JWT_SECRET_KEY']}") 

    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    JWTManager(app)

    from backend.app.routes.auth_routes import auth_bp
    from backend.app.routes.job_routes import jobs_bp
    from backend.app.routes.assessment_routes import assessment_bp
    from backend.app.routes.invitation_routes import invitation_bp
    from backend.app.routes.question_routes import question_bp
    from backend.app.routes.submission_routes import submission_bp
    from backend.app.routes.result_routes import result_bp
    from backend.app.routes.feedback_routes import feedback_bp
    from backend.app.routes.codewars_routes import codewars_bp 

    app.register_blueprint(auth_bp)
    app.register_blueprint(jobs_bp)
    app.register_blueprint(assessment_bp)
    app.register_blueprint(invitation_bp)
    app.register_blueprint(question_bp)
    app.register_blueprint(submission_bp)
    app.register_blueprint(result_bp)
    app.register_blueprint(feedback_bp)
    app.register_blueprint(codewars_bp)
   

    @app.route("/")
    def index():
        return jsonify({"message": "Smart Recruiter is live!"})

    return app
