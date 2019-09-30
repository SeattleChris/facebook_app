
from flask import Flask, request, render_template

# For google cloud: first it looks for 'entrypoint' in app.yaml, then for 'app' here
app = Flask(__name__)


@app.route('/hello')
def hello():
    """Return a friendly HTTP greeting."""
    return render_template('hello.html', name='Chris')


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
