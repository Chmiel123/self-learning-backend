from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse

from src.logic import account_logic
from src.models.account.account import Account
from src.utils.response import ok

email_parser = reqparse.RequestParser()
email_parser.add_argument('email', help='This field cannot be blank', required=True)


class Email(Resource):
    @jwt_required()
    def post(self):
        """Set a new email address for an account, sends verification email.
        ---
        tags:
          - Account
        parameters:
          - name: body
            in: body
            required: true
            schema:
              properties:
                email:
                  type: string
                  example: john@example.com
        responses:
          200:
            description: OK.
        """
        data = email_parser.parse_args()
        account = Account.find_by_username(get_jwt_identity())
        account_logic.generate_email_verification(account, data['email'])
        return ok()


email_verification_parser = reqparse.RequestParser()
email_verification_parser.add_argument('verify', help='This field cannot be blank', location='args', required=True)


class EmailVerify(Resource):
    def get(self):
        """Verifies an email.
        ---
        tags:
          - Account
        parameters:
          - name: verify
            in: query
            required: true
        responses:
          200:
            description: OK.
        """
        data = email_verification_parser.parse_args()
        result = account_logic.verify_email(data['verify'])
        if result:
            return ok()

