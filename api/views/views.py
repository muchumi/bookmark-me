from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from api.constants.status_codes import HTTP_400_BAD_REQUEST

users = Blueprint("users", __name__, url_prefix="/api/v1/users")

bookmarks = Blueprint("bookmarks", __name__, url_prefix="/api/v1/bookmarks")

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

    #Check if password is long or equal to 8 characters
    if len(password) < 8:
        return jsonify({
            "error": "Password is too short"
        }), HTTP_400_BAD_REQUEST
    
    #Check if username is long than 4 characters
    if len(username) < 4:
        return jsonify({
            "error": "Username is too short"
        }), HTTP_400_BAD_REQUEST
    
    # Check if username is Alpha numeric and if there are spaces
    if not username.isalnum() or " " in username:
        return jsonify({
            "error": "Username should be Alpha numeric and no spaces allowed"
        }), HTTP_400_BAD_REQUEST

    


