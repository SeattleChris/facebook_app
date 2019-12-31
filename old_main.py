from facebook import get_user_from_cookie, GraphAPI
from flask import Flask, g, render_template, redirect, abort, request, session, url_for
# from flask.ext.sqlalchemy import SQLAlchemy
import requests
from dotenv import load_dotenv
import os
# from app import app, db
# from .models import User
# For google cloud: first it looks for 'entrypoint' in app.yaml, then for 'app' here
load_dotenv()
app = Flask(__name__)
# app.config.from_object("config")
# db = SQLAlchemy(app)
# TODO: Refactor following to an object to hold all the FaceBook settings?
fb_app_name = os.getenv('FACEBOOK_APP_NAME', '')
fb_app_id = os.getenv('FACEBOOK_APP_ID', '')
fb_app_secret = os.getenv('FACEBOOK_APP_SECRET', '')
fb_api_ver = os.getenv('FACEBOOK_API_VERSION')
# graph = GraphAPI(access_token=fb_app_secret, version=fb_api_ver)
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


class User:
    # __tablename__ = "users"

    def __init__(self, id, name, profile_url, access_token):
        self.id = id
        self.name = name
        self.profile_url = profile_url
        self.access_token = access_token


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


@app.route("/verify", methods=['POST'])
def verify():
    """After the user logs in with the pop-up of the FaceBook site, we want to
    make sure they are the correct user and verify their token.
    """
    # TODO: Add method for PUT to update token and/or permissions.
    # request.json is not MultiDict. request.form can be addressed by key.
    code = request.form['token']
    user_id = request.form['user_id']
    expected = {}
    expected['app_id'] = fb_app_id
    expected['is_valid'] = True
    expected['user_id'] = request.form['user_id']
    expected['scopes'] = vars
    return_page = ''  # TODO: Correct return page?
    url = f"https://graph.facebook.com/{fb_api_ver}/oauth/access_token?"
    url += f"client_id={fb_app_id}&redirect_uri={return_page}&client_secret={fb_app_secret}&code={code}"  # &redirect_uri={return_page}
    response = requests.get(url).json()
    print("===================== code to token? =============================================")
    if response.get('error'):
        return render_template('error.html', error=response.get('error'))
    token = response.get('access_token')
    print(token)
    check_url = 'https://graph.facebook.com/debug_token?'
    check_url += f"input_token={token}&access_token={fb_app_secret}"
    response = requests.get(check_url).json()
    print("===================== json_response ============================")
    if response.get('error'):
        return render_template('error.html', error=response.get('error'))
    for key in response.keys():
        print(key)
    data = response.get('data')
    print("================check_url data=============================")
    good = True
    for key in expected.keys():
        if expected[key] != data[key]:
            good = Falseold_main
            print(f"Expected {key}: {expected[key]} but got {data[key]}")
        else:
            print(f"{key} is {data[key]}")
    print("=================== We are good: {good} ==================")
    # TODO: Check if they approved everything if scope matches perms. Manage issues.
    return render_template('results.html')


# @app.before_request
# def get_current_user():old_main
#     """Set g.user to the currently logged in user.
#     Called before each request, get_current_user sets the global g.user
#     variable to the currently logged in user.  A currently logged in user is
#     determined by seeing if it exists in Flask's session dictionary.
#     If it is the first time the user is logging into this application it will
#     create the user and insert it into the database.  If the user is not logged
#     in, None will be set to g.user.
#     """

#     # Set the user in the session dictionary as a global g.user and bail out
#     # of this function early.
#     if session.get("user"):
#         g.user = session.get("user")
#         return

#     # Attempt to get the short term access token for the current user.
#     result = get_user_from_cookie(
#         cookies=request.cookies, app_id=fb_app_id, app_secret=fb_app_secret
#     )

#     # If there is no result, we assume the user is not logged in.
#     if result:
#         # Check to see if this user is already in our database.
#         # user = User.query.filter(User.id == result["uid"]).first()
#         user = None

#         if not user:
#             # Not an existing user so get info
#             graph = GraphAPI(result["access_token"])
#             profile = graph.get_object("me")
#             if "link" not in profile:
#                 profile["link"] = ""

#             # Create the user and insert it into the database
#             user = User(
#                 id=str(profile["id"]),
#                 name=profile["name"],
#                 profile_url=profile["link"],
#                 access_token=result["access_token"],
#             )
#             # db.session.add(user)
#         elif user.access_token != result["access_token"]:
#             # If an existing user, update the access token
#             user.access_token = result["access_token"]

#         # Add the user to the current session
#         session["user"] = dict(
#             name=user.name,
#             profile_url=user.profile_url,
#             id=user.id,
#             access_token=user.access_token,
#         )

#     # Commit changes to the database and set the user as a global g.user
#     # db.session.commit()
#     g.user = session.get("user", None)
#     print('Current User: ', g.user)


# @app.route('/', methods=['GET', 'POST'])
# def join():
#     """Add a user for our app"""
#     # DEPLOYED_SITE = os.environ.get('DEPLOYED_SITE', '')
#     confirm_url = 'https://fb-test-251219.appspot.com'  # refactor with variables
#     fb_app_name = os.getenv('FACEBOOK_APP_NAME', '')
#     fb_app_id = os.getenv('FACEBOOK_APP_ID', '')
#     fb_app_secret = os.getenv('FACEBOOK_APP_SECRET', '')
#     fb_api_ver = os.getenv('FACEBOOK_API_VERSION', '3.1')
#     graph = GraphAPI(access_token=fb_app_secret, version=fb_api_ver)
#     perms = [
#         'email',
#         'user_link',
#         'user_friends',
#         'user_likes',
#         'user_photos',
#         'user_posts',
#         'user_tagged_places',
#         'user_videos',
#         'groups_access_member_info',
#         'pages_show_list',
#         'read_insights',
#         'instagram_basic',
#         'instagram_manage_comments',
#         'instagram_manage_insights',
#             ]
#     fb_login_url = graph.get_auth_url(fb_app_id, confirm_url, perms)
#     # response = requests.get(fb_login_url)
#     # json_response = response.json()
#     # has_token = False
#     # if json_response['accessToken']:
#     #     has_token = True
#     # print(response.text)
#     # return render_template('confirm.html', token_exists=response.text)
#     return redirect(fb_login_url)

# @app.route('/confirm')
# def confirm():
#     """ Where user is sent after confirming app permissions """
#     print('====== Confirm ========')
#     return render_template('confirm.html')


# @app.route('/', methods=['GET'])
# def home():
#     """ Return our home index page """
#     return render_template('home.html')


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
