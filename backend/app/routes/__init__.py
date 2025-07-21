from app.routes.auth_routes import auth_bp
from app.routes.assessment_routes import assessment_bp
from app.routes.recruiter_routes import recruiter_bp
from app.routes.interviewee_routes import interviewee_bp

app.register_blueprint(auth_bp)
app.register_blueprint(assessment_bp)
app.register_blueprint(recruiter_bp)
app.register_blueprint(interviewee_bp)
