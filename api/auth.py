from flask import Blueprint

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth.route("/", methods=['GET'])
def index():
    return({
        "message": "Hello world, welcome to Bookmark-me REST API"
    }, 200)
    
@auth.route("/register", methods=['GET'])
def register():
    return ({
        "message": "User created"
    },200)

