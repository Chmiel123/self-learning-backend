from datetime import timedelta

from flask_restful import Resource, reqparse, inputs
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, \
    get_jwt_identity
from src.logic import account_logic

from src.services import services

account_get_parser = reqparse.RequestParser()
account_get_parser.add_argument('id', location='args', required=False)
account_get_parser.add_argument('name', location='args', required=False)
account_get_parser.add_argument('domain', location='args', required=False)

register_parser = reqparse.RequestParser()
register_parser.add_argument('username', help='This field cannot be blank', required=True)
register_parser.add_argument('password', help='This field cannot be blank', required=True)
register_parser.add_argument('email', help='This field cannot be blank', required=True)

login_parser = reqparse.RequestParser()
login_parser.add_argument('username', help='This field cannot be blank', required=True)
login_parser.add_argument('password', help='This field cannot be blank', required=True)

email_parser = reqparse.RequestParser()
email_parser.add_argument('email', help='This field cannot be blank', required=True)
email_parser.add_argument('primary', type=inputs.boolean)

email_verification_parser = reqparse.RequestParser()
email_verification_parser.add_argument('verify', help='This field cannot be blank', location='args', required=True)


class AccountRegistration(Resource):
    def post(self):
        data = register_parser.parse_args()
        new_account = account_logic.create_account_with_password(
            data['username'], data['email'], data['password'])

        access_token = create_access_token(identity=data['username'],
                                           expires_delta=timedelta(
                                               days=services.flask.config['JWT_ACCESS_TOKEN_EXPIRES_DAYS']))
        refresh_token = create_refresh_token(identity=data['username'],
                                             expires_delta=timedelta(
                                                 days=services.flask.config['JWT_ACCESS_TOKEN_EXPIRES_DAYS']))
        return {
            'status': 'Ok',
            'message': f'User {data["username"]} was created',
            'access_token': access_token,
            'refresh_token': refresh_token
        }


class AccountLogin(Resource):
    def post(self):
        data = login_parser.parse_args()
        current_account = account_logic.login(data['username'], data['password'])

        access_token = create_access_token(identity=current_account.name,
                                           expires_delta=timedelta(
                                               days=services.flask.config['JWT_ACCESS_TOKEN_EXPIRES_DAYS']))
        refresh_token = create_refresh_token(identity=current_account.name,
                                             expires_delta=timedelta(
                                                 days=services.flask.config['JWT_ACCESS_TOKEN_EXPIRES_DAYS']))
        return {
            'status': 'Ok',
            'message': f'Logged in as {current_account.name}',
            'access_token': access_token,
            'refresh_token': refresh_token
        }


# class AccountLogoutAccess(Resource):
#     @jwt_required
#     def post(self):
#         jti = get_raw_jwt()['jti']
#         try:
#             revoked_token = RevokedTokenModel(jti = jti)
#             revoked_token.add()
#             return {'message': 'Access token has been revoked'}
#         except:
#             return {'message': 'Something went wrong'}, 500


# class AccountLogoutRefresh(Resource):
#     @jwt_refresh_token_required
#     def post(self):
#         jti = get_raw_jwt()['jti']
#         try:
#             revoked_token = RevokedTokenModel(jti = jti)
#             revoked_token.add()
#             return {'message': 'Refresh token has been revoked'}
#         except:
#             return {'message': 'Something went wrong'}, 500

#
# class TokenRefresh(Resource):
#     @jwt_required
#     def get(self):
#         current_user = get_jwt_identity()
#         access_token = create_access_token(identity=current_user, expires_delta=datetime.timedelta(hours=1))
#         refresh_token = create_refresh_token(identity=current_user, expires_delta=datetime.timedelta(hours=1))
#         return {'access_token': access_token, 'refresh_token': refresh_token}
#
#
# class CurrentAccount(Resource):
#     @jwt_required
#     def get(self):
#         account = Account.find_by_username(get_jwt_identity())
#         return {
#             'id': str(account.id),
#             'name': account.name,
#             'domain': account.domain,
#             'created_date': str(account.created_date),
#             'virtual_resource_start_date': str(account.virtual_resource_start_date),
#             'virtual_resource_speed': account.virtual_resource_speed,
#             'virtual_resource_accrued': account.virtual_resource_accrued,
#             'total_resource_spent': account.total_resource_spent
#         }
#
#
# class Accounts(Resource):
#     def get(self):
#         data = account_get_parser.parse_args()
#         account = None
#         if data['id'] and data['id'] != 'null':
#             account = account_logic.get_by_id(data['id'])
#         elif data['name']:
#             account = account_logic.get_by_username(data['name'])
#         else:
#             return response.error("Invalid account id")
#
#         return {
#             'id': str(account.id),
#             'name': account.name,
#             'domain': account.domain
#         }
#
#
# class Email(Resource):
#     @jwt_required
#     def get(self):
#         account = Account.find_by_username(get_jwt_identity())
#         return {
#             'emails': [{'email': x.email, 'verified': x.verified, 'primary': x.primary} for x in account.emails]
#         }
#
#     @jwt_required
#     def post(self):
#         data = email_parser.parse_args()
#         try:
#             # update
#             account = Account.find_by_username(get_jwt_identity())
#             for account_email in account.emails:
#                 if account_email.email == data['email']:
#                     if data['primary']:
#                         email_logic.set_primary(account_email)
#                     if not account_email.verified:
#                         email_logic.generate_verification(account_email)
#                         # TODO: send actual email
#                         return response.ok('Resent verification email')
#                     return response.ok()
#
#             # create
#             max_emails = config['limit']['max_emails_per_account']
#             if len(account.emails) >= max_emails:
#                 return response.error(f'Maximum number of emails ({max_emails}) per account reached')
#
#             new_account_email = AccountEmail(
#                 account=account,
#                 email=data['email']
#             )
#             new_account_email.save_to_db()
#             if data['primary']:
#                 email_logic.set_primary(new_account_email)
#             email_logic.generate_verification(new_account_email)
#             # TODO: send actual email
#             return response.ok('Sent verification email')
#
#         except IMException as e:
#             return response.error(e.args[0])
#
#     @jwt_required
#     def delete(self):
#         data = email_parser.parse_args()
#         account = Account.find_by_username(get_jwt_identity())
#         for email in account.emails:
#             if email.email == data['email']:
#                 AccountEmail.delete_by_email(email.email)
#                 return response.ok('Email deleted')
#         return response.error('Email not found')
#
#
# class EmailVerify(Resource):
#     def get(self):
#         data = email_verification_parser.parse_args()
#         try:
#             email_logic.verify(data['verify'])
#             return response.ok()
#         except IMException as e:
#             return response.error(e.args[0])
#
