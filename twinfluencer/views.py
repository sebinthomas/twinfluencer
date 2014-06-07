#!flask/bin/python

from twinfluencer import app,db
from flask import Flask, request, redirect, url_for, session, flash, g, \
     render_template, jsonify
from models import User
from flask_oauth import OAuth



oauth=OAuth()

twitter = oauth.remote_app("twitter",
    base_url="https://api.twitter.com/1.1/",
    request_token_url="https://api.twitter.com/oauth/request_token",
    access_token_url="https://api.twitter.com/oauth/access_token",
    authorize_url="https://api.twitter.com/oauth/authenticate",
    consumer_key=app.config["CONSUMER_KEY"],
    consumer_secret=app.config["CONSUMER_SECRET"]
)



@app.before_request
def before_request():
    g.user = None
    if "user_id" in session:
        g.user = User.query.get(session["user_id"])

#Oauth token getter
@twitter.tokengetter
def get_twitter_token():
    user=g.user
    if user is not None:
        return (user.token,user.secret)

@app.route("/login")
def login():
    return twitter.authorize(callback=url_for("authorized",next=request.args.get("next") or None))

@app.route("/authorized")
@twitter.authorized_handler
def authorized(resp):
    next_url=request.args.get("next") or url_for("rank")
    if resp is None:
        print "request denied" 
        return redirect(next_url)
    user=User.query.filter_by(name=resp["screen_name"]).first()

    if user is None:
        user=User(name=resp["screen_name"],token=resp["oauth_token"],secret=resp["oauth_token_secret"])
        db.session.add(user)
        db.session.commit()
    session["user_id"]=user.id
    print "user @ %s registered" %user.id
    return redirect(next_url)

# view that returns a JSON object of the retweets which is then processed clientside.
@app.route("/stats")
def stats():
    tweets=None
    if g.user is None:
        return jsonify({"status":{"message":"Bad login","code":501}}) #redirect(url_for('login',next=request.url))
    else:
        id= request.args.get("id")
        if(id==None):
            return jsonify({"status":{"message":"no proper tweet ID has been provided","code":502}})
        else:
            resp=twitter.get("statuses/retweets/"+id+".json")
            if resp.status==200:
                data={"status":{"message":"clear","code":500},"data":resp.data}
            else:
                data={"status":{"message":"Response from twitter is bad.","code":503}}
            print "stats for id %s queried"%id    
            return jsonify(**data)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/rank")
def rank():
    if g.user is None:
        return redirect(url_for("login",next=url_for("rank")))
    else:
        return render_template("tweetpage.html")
