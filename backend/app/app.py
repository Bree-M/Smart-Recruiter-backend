from backend.app import create_app
from flask_cors import CORS

def create_app():
    app=Flask(__name__)
    CORS(app)

    @app.route('/api/recruiters')
    def get_recruiters():
        return [{"id":1,"name":"Test Recruiter"}],200
    
    return app
app=create_app()


