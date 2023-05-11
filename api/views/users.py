from flask import Blueprint

users = Blueprint("users", __name__, url_prefix="/api/v1/users")


@users.route("/", methods=['GET'])
def index():
    return({
        "message": "Hello world, welcome to Bookmark-me REST API"
    }, 200)
    
@users.route("/register", methods=['GET'])
def register():
    return ({
        "message": "User created"
    },200)

