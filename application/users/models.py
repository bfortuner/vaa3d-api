from application import db
from application.users.constants import *

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(264), nullable=False)
    iam_username = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=db.func.now())
    last_updated = db.Column(db.DateTime, onupdate=db.func.now())
    job = db.relationship("Job", backref=db.backref('users'))

    def __init__(self, email, iam_username=DEFAULT_IAM_USER):
        self.email = email
        self.iam_username = iam_username

      
    def __repr__(self):
        return '<User %r>' % (self.name)