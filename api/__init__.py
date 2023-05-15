import os
from flask import Flask
from api.views.users import users
from api.views.bookmarks import bookmarks
from api.models.models import db


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY = os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DATABASE_URI")
        )
    else:
        app.config.from_mapping(test_config)
        db.app=app
        db.init_app(app)
    """
        Registering Blueprints to the app instance
    """
    app.register_blueprint(users)
    app.register_blueprint(bookmarks)

    return app



if __name__ == '__main__':
    app.run(debug=True)