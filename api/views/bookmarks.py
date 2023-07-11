import validators
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.constants.status_codes import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_201_CREATED, HTTP_200_OK, HTTP_404_NOT_FOUND
from api.models.models import Bookmark, db

# Bookmarks Blueprint
bookmarks = Blueprint("bookmarks", __name__, url_prefix="/api/v1/bookmarks")

"""
    All bookmarks endpoints.
"""
# A route to create a bookmark
@bookmarks.route('/', methods=['POST'])
@jwt_required()
def create_bookmarks():
    current_user = get_jwt_identity()
    if request.method == 'POST':
        url = request.get_json().get('url', ' ')
        body = request.get_json().get('body', ' ')
        
        # Checking if the url entered by user is valid
        if not validators.url(url):
            return jsonify({
                "error": "Url provided is invalid"
            }), HTTP_400_BAD_REQUEST
        
        # Checking if the url already exists
        if Bookmark.query.filter_by(url=url).first() is not None:
            return jsonify({
                "error": "Url already exists"
            }), HTTP_409_CONFLICT
        
        bookmark = Bookmark(url=url, body=body, user_id=current_user)
        db.session.add(bookmark)
        db.session.commit()

        return jsonify({
            "id": bookmark.id,
            "url": bookmark.url,
            "short_url": bookmark.short_url,
            "body": bookmark.body,
            "visits": bookmark.bookmark_visits,
            "created_at": bookmark.created_at,
            "updated_at": bookmark.updated_at

        }), HTTP_201_CREATED
    
# A route to retrieve all bookmarks
@bookmarks.route('/', methods=['GET'])
@jwt_required()
def get_bookmarks():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    current_user = get_jwt_identity()
    bookmarks = Bookmark.query.filter_by(user_id=current_user).paginate(page=page, per_page=per_page)
    data = []
    for bookmark in bookmarks.items:
        data.append({
            "id": bookmark.id,
            "url": bookmark.url,
            "short_url": bookmark.short_url,
            "body": bookmark.body,
            "visits": bookmark.bookmark_visits,
            "created_at": bookmark.created_at,
            "updated_at": bookmark.updated_at
        })                   
        meta={
            "page": bookmarks.page,
            "pages": bookmarks.pages,
            "total_count": bookmarks.total,
            "previous_page": bookmarks.prev_num,
            "next_page": bookmarks.next_num,
            "has_next": bookmarks.has_next,
            "has_previous": bookmarks.has_prev
        }
    return jsonify({
        "data": data,
        "meta": meta
    }), HTTP_200_OK


# A route to retrieve a single bookmark
@bookmarks.route("/<int:id>", methods = ['GET'])
@jwt_required()
def get_bookmark(id):
    current_user = get_jwt_identity()
    bookmark = Bookmark.query.filter_by(user_id=current_user, id=id).first()

    if not bookmark:
        return jsonify({
            "error": "Bookmark not found"
        }), HTTP_404_NOT_FOUND
    return jsonify({
        "id": bookmark.id,
        "url": bookmark.url,
        "short_url": bookmark.short_url,
        "body": bookmark.body,
        "visits": bookmark.bookmark_visits,
        "created_at": bookmark.created_at,
        "updated_at": bookmark.updated_at
    }), HTTP_200_OK


# A route to edit a bookmark
@bookmarks.route('/<int:id>', methods = ['PUT'])
@jwt_required()
def edit_bookmark(id):
    current_user = get_jwt_identity()
    bookmark = Bookmark.query.filter_by(user_id=current_user, id=id).first()

    if not bookmark:
        return jsonify({
            "error": "Bookmark not found"
        }), HTTP_404_NOT_FOUND
    
    url = request.get_json().get('url', ' ')
    body = request.get_json().get('body', ' ')

    if not validators.url(url):
        return jsonify({
            "error": "Url provided is invalid"
        }), HTTP_400_BAD_REQUEST
    
    # Updating bookmark properties
    bookmark.url=url
    bookmark.body=body
    db.session.commit()
    return jsonify({
        "id": bookmark.id,
        "url": bookmark.url,
        "short_url": bookmark.short_url,
        "body": bookmark.body,
        "visits": bookmark.bookmark_visits,
        "created_at": bookmark.created_at,
        "updated_at": bookmark.updated_at
    }), HTTP_200_OK

# A route to delete a bookmark
@bookmarks.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_bookmark(id):
    current_user = get_jwt_identity()
    bookmark=Bookmark.query.filter_by(user_id=current_user, id=id).first()

    if not bookmark:
        return jsonify({
            "error": "Bookmark not found"
        }), HTTP_404_NOT_FOUND
    
    db.session.delete(bookmark)
    db.session.commit()
    return jsonify({
        "message": "Bookmark deleted successfully"
    }), HTTP_200_OK

