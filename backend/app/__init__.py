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
    from backend.app.routes.recruiter_routes import recruiter_bp
    from backend.app.routes.interviewee_routes import interviewee_bp
    from backend.app.routes.assessment_routes import assessment_bp
    from backend.app.routes.invitation_routes import invitation_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(jobs_bp)
    app.register_blueprint(recruiter_bp)
    app.register_blueprint(interviewee_bp)
    app.register_blueprint(assessment_bp)
    app.register_blueprint(invitation_bp)
   

    @app.route("/")
    def index():
        return jsonify({"message": "Smart Recruiter is live!"})

    return app
