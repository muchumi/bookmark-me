import validators
from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token
from api.constants.status_codes import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED, HTTP_200_OK
from api.models.models import User, db

# Users Blueprint
users = Blueprint("users", __name__, url_prefix="/api/v1/users")


"""
    All users endpoints.
"""

@users.route("/", methods=['GET'])
def index():
    return({
        "message": "Hello world, welcome to Bookmark-me REST API"
    }, 200)
    
@users.route("/register", methods=['POST'])
def register():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    #Check if password is longer or equal to 8 characters
    if len(password) < 8:
        return jsonify({
            "error": "Password is too short"
        }), HTTP_400_BAD_REQUEST
    
    #Check if username is longer than 4 characters
    if len(username) < 4:
        return jsonify({
            "error": "Username is too short"
        }), HTTP_400_BAD_REQUEST
    
    # Check if username is Alpha numeric and if there are spaces
    if not username.isalnum() or " " in username:
        return jsonify({
            "error": "Username should be Alpha numeric and no spaces allowed"
        }), HTTP_400_BAD_REQUEST

    #Validating the email input
    if not validators.email(email):
        return jsonify({
            "error": "Email is not valid"
        }), HTTP_400_BAD_REQUEST
    
    # Checking if the email input is unique
    if User.query.filter_by(email=email).first() is not None:
        return jsonify({
            "error": "Email already taken"
        }), HTTP_409_CONFLICT
    
    # Checking if the username input is unique
    if User.query.filter_by(username=username).first() is not None:
        return jsonify({
            "error": "Username already taken"
        }), HTTP_409_CONFLICT
    
    # Hashing the user password
    password_hash = generate_password_hash(password)

    user = User(username=username, email=email, password=password_hash)
    db.session.add(user)
    db.session.commit()
    return jsonify({
        "message": "User created",
        "user": {
            "username": username, "email": email
        }
    }), HTTP_201_CREATED

# The route that allows a user to login
@users.route("/login", methods = ['POST'])
def login():
    email = request.json.get('email', ' ')
    password = request.json.get('password', ' ')

    # Checking if this user exists
    user = User.query.filter_by(email=email).first()
    if user:
        is_password_correct = check_password_hash(user.password, password)
        if is_password_correct:
            refresh = create_refresh_token(identity=user.id)
            access = create_access_token(identity=user.id)
            return jsonify({
                "user": {
                    "refresh": refresh,
                    "access": access,
                    "username": user.username,
                    "email": user.email
                }
            }), HTTP_200_OK
        return jsonify({
            "error": "Credentials provided are invalid"
        }), HTTP_401_UNAUTHORIZED

# Protecting the # me route
@users.route("/me", methods = ['GET'])
@jwt_required()
def me():
    user_id=get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    return jsonify({
        "username": user.username,
        "email": user.email
    }), HTTP_200_OK

# Generating user refresh tokens
@users.route("/token/refresh", methods = ['GET'])
@jwt_required(refresh=True)
def refresh_users_token():
    # Getting user's id using get_jwt_identity() method
    identity = get_jwt_identity()
    access = create_access_token(identity=identity)

    return jsonify({
        "access": access
    }), HTTP_200_OK




