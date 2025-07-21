from flask import Flask,jsonify
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
    app = Flask(__name__,instance_relative_config=True)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    JWTManager(app)

    from backend.app import models
    from backend.app.routes.auth_routes import auth_bp
    from backend.app.routes.assessment_routes import assessment_bp
    from backend.app.routes.recruiter_routes import recruiter_bp
    from backend.app.routes.interviewee_routes import interviewee_bp
    from backend.app.routes.codewars_routes import codewars_routes 
    app.register_blueprint(auth_bp)
    app.register_blueprint(assessment_bp)
    app.register_blueprint(recruiter_bp)
    app.register_blueprint(interviewee_bp)
    app.register_blueprint(codewars_routes)
    

    @app.route("/")
    def index():
        return jsonify({"message":"Smart Rcruiter is live!"})

   

    return app