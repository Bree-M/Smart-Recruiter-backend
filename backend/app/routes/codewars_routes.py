from flask import Blueprint, jsonify
import requests

codewars_bp = Blueprint('codewars', __name__, url_prefix='/codewars')

@codewars_bp.route('/<username>', methods=['GET'])
def get_codewars_user(username):
    url = f"https://www.codewars.com/api/v1/users/{username}"
    try:
        response=requests.get(url,timeout=5)
    except requests.RequestException:
        return jsonify({'error':'Connection Failed'}),503
    if response.status_code != 200:
        return jsonify({'error':f'Codewars user "{username}" not found!'}),404    
    
    data=response.json()

    user_info={
        'username': data.get('username'),
        'honor': data.get('honor'),
        'clan': data.get('clan'),
        'rank': data.get('ranks', {}).get('overall', {}).get('name'),
        'total_completed': data.get('codeChallenges', {}).get('totalCompleted'),
        'languages': list(data.get('ranks', {}).get('languages', {}).keys())
    }

    return jsonify({'message':'User Fetched Successfully!','data':user_info}),200