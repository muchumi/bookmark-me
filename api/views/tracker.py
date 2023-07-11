from flask import Blueprint, redirect
from api.models.models import Bookmark, db

# Tracker Blueprint
tracker = Blueprint("tracker", __name__, url_prefix="/api/v1/tracker")

"""
    Click link tracker endpoint
""" 
@tracker.route('/<short_url>', methods = ['GET'])
def redirect_to_url(short_url):
    bookmark = Bookmark.query.filter_by(short_url=short_url).first_or_404()

    if bookmark:
        bookmark.visits = bookmark.visits+1
        db.session.commit()
        return redirect(bookmark.url)


