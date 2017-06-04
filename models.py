from app import db
from sqlalchemy.dialects import postgresql 

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    fitbitid = db.Column(db.String, nullable=False, unique=True)
    fullname = db.Column(db.String)
    access_token = db.Column(db.String)
    refresh_token = db.Column(db.String)
    token_expires_at = db.Column(db.Float)
    target = db.Column(db.Integer)
    activities = db.Column(postgresql.ARRAY(db.String))
    distances = db.Column(postgresql.ARRAY(db.Float))

    def __init__(self, fitbitid, fullname, access_token, refresh_token, token_expires_at, target, 
        activities):
        self.fitbitid = fitbitid
        self.fullname = fullname
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.token_expires_at = token_expires_at
        self.target = target
        self.activities = activities
        self.distances = []

    def __repr__(self):
        return '<User(fullname={}, fitbitid={}, target={}, activities={})'.format(self.fullname,
            self.fitbitid, self.target, self.activities)
