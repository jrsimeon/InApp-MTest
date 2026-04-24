from flask import render_template, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)
from . import auth


# # UI Route (serves login page)
@auth.route('/login')
def login_page():   
    return render_template('login.html')

@auth.route("/logout")
def logout_page():
    return render_template("logout.html")

# API Route (handles login request)
@auth.route('/api/login', methods=['POST'])
def login_api():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    # Basic validation
    if not email or not password:
        return jsonify({"message": "Email and password required"}), 400

    # Can Replace with DB validation
    if email == "email@test.com" and password == "1234":
        access_token = create_access_token(identity=email)

        return jsonify({
            "access_token": access_token,
            "user": {"email": email}
        }), 200

    return jsonify({"message": "Invalid credentials"}), 401

# 🔐 PROTECTED API
@auth.route("/api/profile", methods=["GET"])
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    return jsonify({
        "message": "Protected data",
        "user": current_user
    })

# 🔐 LOGOUT API (basic version)
@auth.route("/api/logout", methods=["POST"])
@jwt_required()
def logout_api():
    # For now: client deletes token
    return jsonify({"message": "Logged out successfully"}), 200