from flask import Flask,jsonify
from flask_cors import CORS

def create_app():
    app=Flask(__name__)
    CORS(app)

    @app.route('/api/recruiters',methods=['GET'])
    def get_recruiters():
        return jsonify([{"id":1,"name":"Test Recruiter"},{"id":2,"name":"Recruiter Test"}]),200
    
    return app
app=create_app()

if __name__=="__main__":
    app.run(debug=True)


