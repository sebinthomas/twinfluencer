#!flask/bin/python

from twinfluencer import db

class User(db.Model):
    id=db.Column('user_id',db.Integer, primary_key=True)
    name=db.Column(db.String(64))
    token=db.Column(db.String(64))
    secret=db.Column(db.String(64))
    
    
