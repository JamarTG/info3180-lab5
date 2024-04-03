# Add any model classes for Flask-SQLAlchemy here
from . import db

class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    title = db.Column(db.String())
    description = db.Column(db.String())
    poster = db.Column(db.String())
    created_at = db.Column(db.DateTime())