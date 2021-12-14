from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from os import environ

from src.services import services
from src.services import db_postgres

services.flask = Flask(__name__)

services.flask.config.from_object('src.configuration.default_settings')
services.flask.config.from_object('src.configuration.production_settings')
if environ.get('SELF_LEARNING_BACKEND_SETTINGS'):
    services.flask.config.from_envvar('SELF_LEARNING_BACKEND_SETTINGS')

services.jwt = JWTManager(services.flask)
services.api = Api(services.flask)
services.db = db_postgres(services.flask)

if __name__ == "__main__":
    services.flask.run(ssl_context='adhoc')