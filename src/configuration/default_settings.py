APP_NAME = 'Self learning backend'
APP_VERSION = '0.1'

# postgresql+psycopg2://user:password@host/database
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:abc@localhost'
SQLALCHEMY_DATABASE_NAME = 'SelfLearning'

BCRYPT_ROUNDS = 10

SECRET_KEY = 'development-secret'
JWT_SECRET_KEY = 'development-secret'
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
JWT_ACCESS_TOKEN_EXPIRES_HOURS = 24 * 7

EMAIL_VERIFICATION_HOURS = 72
PASSWORD_RESET_HOURS = 72
