from flask import Blueprint, redirect
from api.models.models import Bookmark, db

# Url Shortener Blueprint
shortUrl = Blueprint("shortUrl", __name__, url_prefix="/api/v1/shortUrl")

"""
    Click link tracker endpoint
""" 
@shortUrl.route('/<short_url>', methods = ['GET'])
def redirect_to_url(short_url):
    bookmark = Bookmark.query.filter_by(short_url=short_url).first_or_404()

    if bookmark:
        bookmark.visits = bookmark.visits+1
        db.session.commit()
        return redirect(bookmark.url)


