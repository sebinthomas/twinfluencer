#!flask/bin/python

from flask.ext.script import Manager
from twinfluencer import app,db

manager=Manager(app)


@manager.command
def createdb():
    db.create_all()

@manager.command
def destroydb():
    db.drop_all()

@manager.command
def run():
    app.run(debug=True)
    
if __name__=='__main__':
    manager.run()
