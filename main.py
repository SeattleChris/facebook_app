
from flask import Flask, request, render_template
import facebook
import os


# For google cloud: first it looks for 'entrypoint' in app.yaml, then for 'app' here
app = Flask(__name__)


@app.route('/hello')
def hello():
    """Return a friendly HTTP greeting."""
    return render_template('hello.html', name='Chris')


@app.route('/join')
def join():
    """Add a user for our app"""
    # DEPLOYED_SITE = os.environ.get('DEPLOYED_SITE', '')
    confirm_url = 'https://fb-test-251219.appspot.com/confirm'  # refactor with variables
    fb_app_id = os.environ.get('FACEBOOK_APP_ID', '')
    fb_app_token = os.environ.get('FACEBOOK_APP_SECRET', '')
    fb_api_ver = os.environ.get('FACEBOOK_API_VERSION', '3.1')
    graph = facebook.GraphAPI(access_token=fb_app_token, version=fb_api_ver)
    perms = [
        'default',
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
    fb_login_url = graph.get_auth_url(fb_app_id, confirm_url, perms)
    print('====================================================')
    print(fb_login_url)
    print('====================================================')
    return render_template('confirm.html')


@app.route('/confirm')
def confirm():
    """ Where user is sent after confirming app permissions """
    print('====== Confirm ========')
    return render_template('confirm.html')



@app.route('/', methods=['GET'])
def home():
    """ Return our home index page """
    return render_template('home.html')


@app.route('/<string:page_name>/')
def render_static(page_name):
    """ Return the requested page """
    return render_template('%s.html' % page_name)


if __name__ == '__main__':
    # Used for running locally. When deployed on Google App Engine, a webserver
    #  process (like Gunicorn) will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
