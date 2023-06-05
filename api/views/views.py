from flask import Blueprint

users = Blueprint("users", __name__, url_prefix="/api/v1/users")

bookmarks = Blueprint("bookmarks", __name__, url_prefix="/api/v1/bookmarks")

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


@bookmarks.route("/", methods=['GET'])
def index():
    return({
        "message": "Hello world, welcome to Bookmark-me REST API"
    }, 200)

@bookmarks.route("/get_all", methods=['GET'])
def get_all():
    return {
        "bookmarks": []
    }