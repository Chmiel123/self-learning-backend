import logging

APP_NAME = 'Self learning backend'
APP_VERSION = '0.1'

# postgresql+psycopg2://user:password@host/database
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:abc@localhost'
SQLALCHEMY_DATABASE_NAME = 'SelfLearning'

FILE_LOGGING = False
FILE_LOGGING_FILENAME = 'logs/self-learning-backend.log'
FILE_LOGGING_LEVEL = logging.ERROR

BCRYPT_ROUNDS = 10
SECRET_KEY = 'development-secret'
JWT_SECRET_KEY = 'development-secret'
JWT_ACCESS_TOKEN_EXPIRES_HOURS = 24 * 7
JWT_AUTH_HEADER_NAME = 'Authorization'
JWT_AUTH_URL_RULE = '/account/login'

ADMIN_STRENGTH_MIN = 1
ADMIN_STRENGTH_MAX = 10

SWAGGER_DOCUMENTATION = True

EMAIL_VERIFICATION_HOURS = 72
PASSWORD_RESET_HOURS = 72

DEFAULT_PAGE_SIZE = 100
MAX_COMMENT_DEPTH = 2
