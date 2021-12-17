from flask import jsonify

from src.resource.account_resource import AccountRegistration, AccountLogin
from src.services import services
from src.util.exceptions import ErrorException, WarningException

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


@flask.errorhandler(ErrorException)
def error_exception_handler(error: ErrorException):
    return jsonify({
        'status': 'Error',
        'error_code': error.error_code,
        'parameters': error.parameters,
        'default_message': error.default_message
    }), 500


@flask.errorhandler(WarningException)
def error_exception_handler(error: WarningException):
    return jsonify({
        'status': 'Warning',
        'warning_code': error.warning_code,
        'parameters': error.parameters,
        'default_message': error.default_message
    }), 200


@flask.errorhandler(404)
def page_not_found(e):
    return jsonify({
        'status': 'Error',
        'error_code': 404,
        'parameters': [],
        'default_message': 'Endpoint not found'
    }), 404


@flask.route('/ping')
def ping():
    return jsonify(name=flask.config['APP_NAME'], version='0.1')


api.add_resource(AccountRegistration, '/account/register')
api.add_resource(AccountLogin, '/account/login')