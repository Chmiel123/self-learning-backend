import logging

import psycopg2.errors
import sqlalchemy.exc
from flasgger import Swagger
from flask import jsonify
from flask_jwt_extended import JWTManager
from flask_restful import Api

from src.services import services
from src.services.db_postgres import DBPostgres
from src.utils.exceptions import ErrorException, WarningException

services.jwt = JWTManager(services.flask)
services.api = Api(services.flask)
services.db = DBPostgres(services.flask)

if services.flask.config['SWAGGER_DOCUMENTATION']:
    swagger = Swagger(services.flask)

from src.services.email_service import FakeEmailService
services.email = FakeEmailService(services.flask)

from src.resources.system.system_resource import LanguageResource, EnumResource
from src.models.account.logout_token import LogoutToken
from src.resources.account.account_resource import AccountRegistration, AccountLogin, AccountLogout, AccountDetails, \
    AccountRefresh, AccountCurrentDetails
from src.resources.account.email_verification_resource import Email, EmailVerify
from src.resources.account.password_reset_resource import PasswordResetGen, PasswordResetVerify
from src.resources.content.category_resource import CategoryResource
from src.resources.content.course_resource import CourseResource
from src.resources.content.lesson_resource import LessonResource
from src.resources.content.question_resource import QuestionResource
from src.resources.content.account_entity_tag_resource import AccountEntityTagResource

flask = services.flask
jwt = services.jwt
api = services.api
db = services.db


@jwt.expired_token_loader
def expired_token_callback(expired_token):
    token_type = expired_token['type']
    return jsonify({
        'status': 'Error',
        'message': 'The {} token has expired'.format(token_type)
    }), 401


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token = LogoutToken.find_by_jti(jti)
    return token is not None


@flask.errorhandler(ErrorException)
def error_exception_handler(error: ErrorException):
    return jsonify({
        'status': 'Error',
        'error_code': error.__class__.__name__,
        'parameters': error.parameters,
        'default_message': error.default_message.format(*error.parameters)
    }), 500


@flask.errorhandler(WarningException)
def error_exception_handler(error: WarningException):
    return jsonify({
        'status': 'Warning',
        'warning_code': error.__class__.__name__,
        'parameters': error.parameters,
        'default_message': error.default_message.format(*error.parameters)
    }), 200


@flask.errorhandler(404)
def page_not_found(e):
    return jsonify({
        'status': 'Error',
        'error_code': 404,
        'parameters': [],
        'default_message': 'Endpoint not found'
    }), 404

# TODO: generic exception log to file, not to anyone in the internet
@flask.errorhandler(Exception)
def error_exception_handler(exception: Exception):
    if issubclass(type(exception), psycopg2.errors.Error)\
            or issubclass(type(exception), sqlalchemy.exc.SQLAlchemyError):
        services.db.session.rollback()
    if services.flask.config['DEBUG']:
        logging.exception(exception)
    return jsonify({
        'status': 'Error',
        'error_code': 'unknown_error',
        'parameters': [],
        'default_message': str(exception)
    }), 500


@flask.route('/ping')
def ping():
    return jsonify(name=flask.config['APP_NAME'], version=flask.config['APP_VERSION'])


api.add_resource(LanguageResource, '/system/language')
api.add_resource(EnumResource, '/system/enum')
api.add_resource(AccountRegistration, '/account/register')
api.add_resource(AccountLogin, '/account/login')
api.add_resource(AccountRefresh, '/account/refresh')
api.add_resource(AccountLogout, '/account/logout')
api.add_resource(AccountCurrentDetails, '/account/current')
api.add_resource(AccountDetails, '/account/details')
api.add_resource(Email, '/account/email')
api.add_resource(EmailVerify, '/account/email/verify')
api.add_resource(PasswordResetGen, '/account/password-reset')
api.add_resource(PasswordResetVerify, '/account/password-reset/verify')
api.add_resource(CategoryResource, '/category')
api.add_resource(CourseResource, '/course')
api.add_resource(LessonResource, '/lesson')
api.add_resource(QuestionResource, '/question')
api.add_resource(AccountEntityTagResource, '/tag')
