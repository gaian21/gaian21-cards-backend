from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime

class DatabaseManager:
    def __init__(self, connection_string):
        """Initialize database connection"""
        self.client = MongoClient(connection_string)
        self.db = self.client['panini_cards']
        self.users = self.db['users']
        
        # Create unique index on email
        self.users.create_index("email", unique=True)

    def register_user(self, email, password, username):
        """Register a new user"""
        try:
            user = {
                "email": email,
                "password": generate_password_hash(password),
                "username": username,
                "created_at": datetime.utcnow(),
                "collections": [],
                "favorites": []
            }
            
            result = self.users.insert_one(user)
            return {"success": True, "user_id": str(result.inserted_id)}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def login_user(self, email, password):
        """Authenticate a user"""
        user = self.users.find_one({"email": email})
        
        if user and check_password_hash(user['password'], password):
            return {"success": True, "user_id": str(user['_id'])}
        return {"success": False, "error": "Invalid email or password"}

    def get_user_profile(self, user_id):
        """Get user profile data"""
        user = self.users.find_one({"_id": user_id})
        if user:
            # Remove sensitive data
            user.pop('password', None)
            user['_id'] = str(user['_id'])
            return user
        return None
