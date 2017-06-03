from app import db
from sqlalchemy.dialects import postgresql 

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    access_token = db.Column(db.String)
    refresh_token = db.Column(db.String)
    token_expires_at = db.Column(db.Float)
    target = db.Column(db.Integer)
    activities = db.Column(postgresql.ARRAY(db.String))
    distances = db.Column(postgresql.ARRAY(db.Float))

    def __init__(self, username, access_token, refresh_token, token_expires_at, target, activities):
        self.username = username
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.token_expires_at = token_expires_at
        self.target = target
        self.activities = activities
        self.distances = []

    def __repr__(self):
        return '<User(username={}, target={}, activities={})'.format(self.username, self.target, 
            self.activities)
