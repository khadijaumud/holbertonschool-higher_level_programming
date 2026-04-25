from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_httpauth import HTTPBasicAuth
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'holberton-super-secret'

auth = HTTPBasicAuth()
jwt = JWTManager(app)

users = {
    "user1": {
        "username": "user1", 
        "password": generate_password_hash("password"), 
        "role": "user"
    },
    "admin1": {
        "username": "admin1", 
        "password": generate_password_hash("password"), 
        "role": "admin"
    }
}

# --- BASIC AUTH LOGIC ---
@auth.verify_password
def verify_password(username, password):
    user = users.get(username)
    if user and check_password_hash(user['password'], password):
        return user
    return None

# --- JWT CUSTOM ERROR HANDLERS (CRITICAL FOR PASSING) ---

@jwt.unauthorized_loader
def handle_unauthorized_error(err):
    return jsonify({"error": "Missing or invalid token"}), 401

@jwt.invalid_token_loader
def handle_invalid_token_error(err):
    return jsonify({"error": "Invalid token"}), 401

@jwt.expired_token_loader
def handle_expired_token_error(err):
    return jsonify({"error": "Token has expired"}), 401

@jwt.revoked_token_loader
def handle_revoked_token_error(err):
    return jsonify({"error": "Token has been revoked"}), 401

@jwt.needs_fresh_token_loader
def handle_needs_fresh_token_error(err):
    return jsonify({"error": "Fresh token required"}), 401

# --- ROUTES ---

# 1. Basic Protected Route
@app.route('/basic-protected')
@auth.login_required
def basic_protected():
    return "Basic Auth: Access Granted"

# 2. Login Route (JWT Token generation)
@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"error": "Missing JSON in request"}), 400
    
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = users.get(username)
    if user and check_password_hash(user['password'], password):
        access_token = create_access_token(identity={'username': username, 'role': user['role']})
        return jsonify(access_token=access_token)
    
    return jsonify({"error": "Invalid credentials"}), 401

# 3. JWT Protected Route
@app.route('/jwt-protected')
@jwt_required()
def jwt_protected():
    return "JWT Auth: Access Granted"

# 4. Role-based Route (Admin only)
@app.route('/admin-only')
@jwt_required()
def admin_only():
    current_user = get_jwt_identity()
    if current_user.get('role') != 'admin':
        return jsonify({"error": "Admin access required"}), 403
    return "Admin Access: Granted"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
