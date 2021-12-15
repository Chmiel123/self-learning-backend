APP_NAME = 'Self learning backend'

# postgresql+psycopg2://user:password@host/database
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:abc@localhost'
SQLALCHEMY_DATABASE_NAME = 'SelfLearning'

BCRYPT_ROUNDS = 10

SECRET_KEY = 'development-secret'
JWT_SECRET_KEY = 'development-secret'
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']