from flask import Blueprint

bookmarks = Blueprint("bookmarks", __name__, url_prefix="/api/v1/bookmarks")



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

