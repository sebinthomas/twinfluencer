#!flask/bin/python
import os

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app= Flask(__name__)
app.config.from_pyfile("config.cfg")
if os.environ.get("DATABASE_URL"):
    app.config["SQLALCHEMY_DATABASE_URI"]=os.environ["DATABASE_URL"]

db=SQLAlchemy(app)

from twinfluencer import views,models
