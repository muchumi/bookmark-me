import os
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flasgger import Swagger, swag_from
from api.views.users import users
from api.views.bookmarks import bookmarks
from api.views.shortUrl import shortUrl
from api.models.models import db
from api.constants.status_codes import *
from api.config.swagger import template, swagger_config


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY = os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DATABASE_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS = False,
            JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY"),
            SWAGGER={
                'title': "Bookmark-me API",
                'uiversion': 3.0
            }
        )
    else:
        app.config.from_mapping(test_config)

    db.app=app
    db.init_app(app)
    JWTManager(app)

    """
        Registering Blueprints to the app instance
    """
    app.register_blueprint(users)
    app.register_blueprint(bookmarks)
    app.register_blueprint(shortUrl)

    Swagger(app, config=swagger_config, template=template)

    """
        Error handlers
    """

    @app.errorhandler(HTTP_404_NOT_FOUND)
    def handle_404(e):
        return jsonify({
            "error": "Not Found"
        }), HTTP_404_NOT_FOUND

    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_500(e):
        return jsonify({
            "error": "Something went wrong!"
        }), HTTP_500_INTERNAL_SERVER_ERROR

    return app

 