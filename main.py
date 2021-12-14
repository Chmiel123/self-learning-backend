# main.py
from flask import Flask
from os import environ


app = Flask(__name__)
app.config.from_object('src.configuration.default_settings')
if environ.get('SELF_LEARNING_BACKEND_SETTINGS'):
    app.config.from_envvar('SELF_LEARNING_BACKEND_SETTINGS')


@app.route('/basic_api/hello_world')
def hello_world():
    return 'Hello, World!'


if __name__ == "__main__":
    app.run(ssl_context='adhoc')
