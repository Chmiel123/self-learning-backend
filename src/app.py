from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

jwt = JWTManager(app)
api = Api(app)
db = DB_Postgres(app)


@jwt.expired_token_loader
def my_expired_token_callback(expired_token):
    token_type = expired_token['type']
    return jsonify({
        'status': 'Error',
        'message': 'The {} token has expired'.format(token_type)
    }), 401


@app.route('/ping')
def ping():
    return jsonify(name=app.config['APP_NAME'], version='0.1')

