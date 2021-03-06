from facebook import get_user_from_cookie, GraphAPI
from flask import Flask, g, render_template, redirect, abort, request, session, url_for
# from flask.ext.sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime
import requests
from dotenv import load_dotenv
import os
# from app import app, db
# from .models import User
# For google cloud: first it looks for 'entrypoint' in app.yaml, then for 'app' here
load_dotenv()
app = Flask(__name__)
app.config.from_object("config")
db = SQLAlchemy(app)
# TODO: Refactor following to an object to hold all the FaceBook settings?
fb_app_name = os.getenv('FACEBOOK_APP_NAME', '')
fb_app_id = os.getenv('FACEBOOK_APP_ID', '')
fb_app_secret = os.getenv('FACEBOOK_APP_SECRET', '')
fb_api_ver = os.getenv('FACEBOOK_API_VERSION')
# graph = GraphAPI(access_token=fb_app_secret, version=fb_api_ver)
db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASS")
db_name = os.getenv("DB_NAME")
cloud_sql_connection_name = os.getenv("CLOUD_SQL_CONNECTION_NAME")
perms = [
    'email',
    'user_link',
    'user_friends',
    'user_likes',
    'user_photos',
    'user_posts',
    'user_tagged_places',
    'user_videos',
    'groups_access_member_info',
    'pages_show_list',
    'read_insights',
    'instagram_basic',
    'instagram_manage_comments',
    'instagram_manage_insights',
        ]


db = SQLAlchemy.create_engine(
    # Equivalent URL:
    # mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=/cloudsql/<cloud_sql_instance_name>
    SQLAlchemy.engine.url.URL(
        drivername='mysql+pymysql',
        username=db_user,
        password=db_pass,
        database=db_name,
        query={
            'unix_socket': '/cloudsql/{}'.format(cloud_sql_connection_name)
        }
    ),
    # ... Specify additional properties here.
)

# class User:
#     # __tablename__ = "users"

#     def __init__(self, id, name, profile_url, access_token):
#         self.id = id
#         self.name = name
#         self.profile_url = profile_url
#         self.access_token = access_token


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.String, nullable=False, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
        onupdate=datetime.utcnow,
    )
    name = db.Column(db.String, nullable=False)
    profile_url = db.Column(db.String, nullable=False)
    access_token = db.Column(db.String, nullable=False)

@app.route('/hello')
def hello():
    """Return a friendly HTTP greeting."""
    return render_template('hello.html', name='Chris')


@app.route("/")
def index():
    scope = ','.join(str(x) for x in perms)
    # If a user was set in the get_current_user function before the request,
    # the user is logged in.
    # if g.user:
    #     return render_template(
    #         "index.html", app_id=fb_app_id, app_name=fb_app_name, api_ver=fb_api_ver,
    #         scope=scope, user=g.user)
    # Otherwise, a user is not logged in.
    return render_template("login.html", app_id=fb_app_id, app_name=fb_app_name, api_ver=fb_api_ver,
                           scope=scope)


@app.route("/logout")
def logout():
    """Log out the user from the application.
    Log out the user from the application by removing them from the
    session.  Note: this does not log the user out of Facebook - this is done
    by the JavaScript SDK.
    """
    session.pop("user", None)
    return redirect(url_for("index"))


@app.route("/test", methods=['GET', 'POST'])
def test():
    """ Testing the python facebook-sdk """
    if request.method == "POST":
        token = request.form['token']
        user_id = request.form['user_id']
        return '''<h1>We had a Post!</h1><p>
                Token is: {}.
                user_id is: {}.</p>'''.format(token, user_id)
    confirm_url = "/test"
    api_ver = "3.1"
    graph = GraphAPI(access_token=fb_app_secret, version=api_ver)

    fb_login_url = graph.get_auth_url(fb_app_id, confirm_url, perms)
    response = requests.get(fb_login_url)
    print("=======================================")
    print(response.text)
    # return render_template("results.html")
    return response.text


@app.before_request
def get_current_user():
    """Set g.user to the currently logged in user.
    Called before each request, get_current_user sets the global g.user
    variable to the currently logged in user.  A currently logged in user is
    determined by seeing if it exists in Flask's session dictionary.
    If it is the first time the user is logging into this application it will
    create the user and insert it into the database.  If the user is not logged
    in, None will be set to g.user.
    """

    # Set the user in the session dictionary as a global g.user and bail out
    # of this function early.
    if session.get("user"):
        g.user = session.get("user")
        return

    # Attempt to get the short term access token for the current user.
    result = get_user_from_cookie(
        cookies=request.cookies, app_id=fb_app_id, app_secret=fb_app_secret
    )

    # If there is no result, we assume the user is not logged in.
    if result:
        # Check to see if this user is already in our database.
        # user = User.query.filter(User.id == result["uid"]).first()
        user = None

        if not user:
            # Not an existing user so get info
            graph = GraphAPI(result["access_token"])
            profile = graph.get_object("me")
            if "link" not in profile:
                profile["link"] = ""

            # Create the user and insert it into the database
            user = User(
                id=str(profile["id"]),
                name=profile["name"],
                profile_url=profile["link"],
                access_token=result["access_token"],
            )
            db.session.add(user)
        elif user.access_token != result["access_token"]:
            # If an existing user, update the access token
            user.access_token = result["access_token"]

        # Add the user to the current session
        session["user"] = dict(
            name=user.name,
            profile_url=user.profile_url,
            id=user.id,
            access_token=user.access_token,
        )

    # Commit changes to the database and set the user as a global g.user
    db.session.commit()
    g.user = session.get("user", None)
    print('Current User: ', g.user)


@app.route('/<string:page_name>/')
def render_static(page_name):
    """ Return the requested page """
    if page_name == 'favicon.ico':
        return abort(404)
    return render_template('%s.html' % page_name)


if __name__ == '__main__':
    # Used for running locally. When deployed on Google App Engine, a webserver
    #  process (like Gunicorn) will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
