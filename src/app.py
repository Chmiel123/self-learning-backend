from flask import jsonify

from src.services import services


flask = services.flask
jwt = services.jwt
api = services.api
db = services.db


@jwt.expired_token_loader
def my_expired_token_callback(expired_token):
    token_type = expired_token['type']
    return jsonify({
        'status': 'Error',
        'message': 'The {} token has expired'.format(token_type)
    }), 401


@flask.route('/ping')
def ping():
    return jsonify(name=flask.config['APP_NAME'], version='0.1')

