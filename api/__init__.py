import os
from flask import Flask
from api.auth import auth
from api.bookmarks import bookmarks


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY = os.environ.get("SECRET_KEY")
        )
    else:
        app.config.from_mapping(test_config)
    """
        Registering Blueprints to the app instance
    """
    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)

    return app



if __name__ == '__main__':
    app.run(debug=True)