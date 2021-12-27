from datetime import timedelta

from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, \
    get_jwt_identity, get_jwt
from flask_restful import Resource, reqparse

from src.logic import account_logic
from src.models.account.account import Account
from src.models.account.logout_token import LogoutToken
from src.services import services
from src.utils.error_code import ErrorCode
from src.utils.exceptions import ErrorException, UserIdOrNameNotFoundException
from src.utils.response import ok

register_parser = reqparse.RequestParser()
register_parser.add_argument('username', help='This field cannot be blank', required=True)
register_parser.add_argument('password', help='This field cannot be blank', required=True)
register_parser.add_argument('email', help='This field cannot be blank', required=True)


class AccountRegistration(Resource):
    def post(self):
        """Register a new account
        ---
        tags:
          - Account
        parameters:
          - name: body
            in: body
            required: true
            schema:
              properties:
                username:
                  type: string
                  example: john
                password:
                  type: string
                  example: pass
                email:
                  type: string
                  example: john@example.com
        responses:
          200:
            description: OK.
        """
        data = register_parser.parse_args()
        new_account = account_logic.create_account_with_password(
            data['username'], data['email'], data['password'])

        access_token = create_access_token(identity=data['username'],
                                           expires_delta=timedelta(
                                               hours=services.flask.config['JWT_ACCESS_TOKEN_EXPIRES_HOURS']))
        refresh_token = create_refresh_token(identity=data['username'],
                                             expires_delta=timedelta(
                                                 hours=services.flask.config['JWT_ACCESS_TOKEN_EXPIRES_HOURS']))
        return ok({
            'message': f'User {data["username"]} was created',
            'access_token': access_token,
            'refresh_token': refresh_token
        })


login_parser = reqparse.RequestParser()
login_parser.add_argument('username', help='This field cannot be blank', required=True)
login_parser.add_argument('password', help='This field cannot be blank', required=True)


class AccountLogin(Resource):
    def post(self):
        """Login
        ---
        tags:
          - Account
        parameters:
          - name: body
            in: body
            required: true
            schema:
              properties:
                username:
                  description: username or email
                  type: string
                  example: john
                password:
                  type: string
                  example: pass
        responses:
          200:
            description: OK.
        """
        data = login_parser.parse_args()
        current_account = account_logic.login(data['username'], data['password'])

        access_token = create_access_token(identity=current_account.name,
                                           expires_delta=timedelta(
                                               hours=services.flask.config['JWT_ACCESS_TOKEN_EXPIRES_HOURS']))
        refresh_token = create_refresh_token(identity=current_account.name,
                                             expires_delta=timedelta(
                                                 hours=services.flask.config['JWT_ACCESS_TOKEN_EXPIRES_HOURS']))
        result = ok({
            'message': f'Logged in as {current_account.name}',
            'access_token': access_token,
            'refresh_token': refresh_token
        })
        response = services.flask.make_response(result)
        response.headers['jwt-token'] = access_token
        return response


class AccountLogout(Resource):
    @jwt_required()
    def post(self):
        """Logout
        ---
        tags:
          - Account
        responses:
          200:
            description: OK.
        """
        jti = get_jwt()['jti']
        revoked_token = LogoutToken(jti)
        revoked_token.save_to_db()
        return ok({'message': 'Access token has been revoked'})


class AccountRefresh(Resource):
    @jwt_required()
    def get(self):
        """Refresh login token
        ---
        tags:
          - Account
        responses:
          200:
            description: OK.
        """
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user,
                                           expires_delta=timedelta(
                                               hours=services.flask.config['JWT_ACCESS_TOKEN_EXPIRES_HOURS']))
        refresh_token = create_refresh_token(identity=current_user,
                                             expires_delta=timedelta(
                                                 hours=services.flask.config['JWT_ACCESS_TOKEN_EXPIRES_HOURS']))
        result = ok({
            'message': f'Refreshed token as {current_user}',
            'access_token': access_token,
            'refresh_token': refresh_token
        })
        response = services.flask.make_response(result)
        response.headers['jwt-token'] = access_token
        return response


class AccountCurrentDetails(Resource):
    @jwt_required()
    def get(self):
        """Get details about the currently logged in account
        ---
        tags:
          - Account
        responses:
          200:
            description: OK.
        """
        account = Account.find_by_username(get_jwt_identity())
        return ok({
            'id': account.id,
            'name': account.name,
            'email': account.email,
            'created_date': str(account.created_date)
        })


account_get_parser = reqparse.RequestParser()
account_get_parser.add_argument('id', location='args', required=False)
account_get_parser.add_argument('name', location='args', required=False)


class AccountDetails(Resource):
    def get(self):
        """Get details about an account
        ---
        tags:
          - Account
        parameters:
          - name: id
            type: int
            in: query
          - name: name
            type: string
            in: query
        responses:
          200:
            description: OK.
        """
        data = account_get_parser.parse_args()
        account = None
        if data['id'] and data['id'] != 'null':
            account = Account.find_by_id(data['id'])
        elif data['name']:
            account = Account.find_by_username(data['name'])
        if not account:
            raise UserIdOrNameNotFoundException([data['id'], data['name']])

        return ok({
            'id': str(account.id),
            'name': account.name
        })
