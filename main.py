
from flask import Flask

# For google cloud: first it looks for 'entrypoint' in app.yaml, then for 'app' here
app = Flask(__name__)


@app.route('/hello')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'


@app.route('/')
def home():
    """ Return our home index page """
    

if __name__ == '__main__':
    # Used for running locally. When deployed on Google App Engine, a webserver
    #  process (like Gunicorn) will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
