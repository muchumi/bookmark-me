import datetime
import string
import random
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(50), unique=True, nullable=False)
    email=db.Column(db.String(80), unique=True, nullable=False)
    password=db.Column(db.Text(), nullable=False)
    created_at=db.Column(db.DateTime, default=datetime.now)
    updated_at=db.Column(db.DateTime, onupdate=datetime.now)
    bookmarks = db.relationship('Bookmark', backref='user')

    def __repr__(self) -> str:
        return 'User>>> {self.username}'
    
class Bookmark(db.Model):
    __tablename__='bookmark'
    id=db.Column(db.Integer, primary_key=True)
    body=db.Column(db.Text, nullable=True)
    url=db.Column(db.Text, nullable=False)
    short_url=db.Column(db.String(5), nullable=False)
    bookmark_visits=db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at=db.Column(db.DateTime, default=datetime.now)
    updated_at=db.Column(db.DateTime, onupdate=datetime.now)

    def generate_short_characters(self):
        characters=string.digits+string.ascii_letters
        picked_characters=''.join(random.choices(characters, k=5))
        link = self.query.filter_by(short_url=picked_characters).first()

        if link:
            self.generate_short_characters()
        else:
            return picked_characters


    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.short_url=self.generate_short_characters()

    def __repr__(self) -> str:
        return 'Bookmark>>> {self.url}'


    