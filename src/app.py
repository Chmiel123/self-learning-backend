from flask import Flask


@app.route('/ping')
def index():
    return 'pong'
