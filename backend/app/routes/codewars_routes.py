from flask import Blueprint, request, jsonify
import requests

codewars_routes = Blueprint('codewars_routes', __name__)

@codewars_routes.route('/codewars/<username>', methods=['GET'])
def get_codewars_user(username):
    url = f"https://www.codewars.com/api/v1/users/{username}"
    response = requests.get(url)

    if response.status_code != 200:
        return jsonify({'error': 'Codewars user not found'}), 404

    data = response.json()
    return jsonify({
        'username': data.get('username'),
        'honor': data.get('honor'),
        'clan': data.get('clan'),
        'rank': data.get('ranks', {}).get('overall', {}).get('name'),
        'total_completed': data.get('codeChallenges', {}).get('totalCompleted'),
        'languages': list(data.get('ranks', {}).get('languages', {}).keys())
    })