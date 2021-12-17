from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.logic import account_logic
from src.models.account.account import Account
from src.utils.response import ok


password_reset_gen_parser = reqparse.RequestParser()
password_reset_gen_parser.add_argument('email', help='This field cannot be blank', required=True)


class PasswordResetGen(Resource):
    def post(self):
        data = password_reset_gen_parser.parse_args()
        account_logic.generate_password_reset(data['email'])
        return ok()


password_reset_verify_parser = reqparse.RequestParser()
password_reset_verify_parser.add_argument('verification_key', help='This field cannot be blank', required=True)
password_reset_verify_parser.add_argument('password', help='This field cannot be blank', required=True)


class PasswordResetVerify(Resource):
    def post(self):
        data = password_reset_verify_parser.parse_args()
        result = account_logic.verify_password_reset(data['verification_key'], data['password'])
        if result:
            return ok()
