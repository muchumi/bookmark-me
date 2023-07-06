import validators
from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token
from api.constants.status_codes import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED, HTTP_200_OK, HTTP_404_NOT_FOUND
from api.models.models import User, Bookmark, db


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


    






