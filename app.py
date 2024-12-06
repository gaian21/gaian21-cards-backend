from flask import Flask, request, jsonify
from flask_cors import CORS
from db_manager import DatabaseManager
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

db = DatabaseManager(os.getenv('MONGO_URI'))

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    result = db.register_user(
        email=data.get('email'),
        password=data.get('password'),
        username=data.get('username')
    )
    return jsonify(result)

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    result = db.login_user(
        email=data.get('email'),
        password=data.get('password')
    )
    return jsonify(result)

@app.route('/api/profile/<user_id>', methods=['GET'])
def get_profile(user_id):
    profile = db.get_user_profile(user_id)
    if profile:
        return jsonify(profile)
    return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
