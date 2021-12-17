#
# password_reset_gen_parser = reqparse.RequestParser()
# password_reset_gen_parser.add_argument('email', help='This field cannot be blank', required=True)
#
# password_reset_verify_parser = reqparse.RequestParser()
# password_reset_verify_parser.add_argument('verification_key', help='This field cannot be blank', required=True)
# password_reset_verify_parser.add_argument('password', help='This field cannot be blank', required=True)
#
# class PasswordResetGen(Resource):
#     def post(self):
#         data = password_reset_gen_parser.parse_args()
#         try:
#             account_logic.generate_password_reset(data['email'])
#             return response.py.ok()
#         except IMException as e:
#             return response.py.error(e.args[0])
#
#
# class PasswordResetVerify(Resource):
#     def post(self):
#         data = password_reset_verify_parser.parse_args()
#         try:
#             result = account_logic.verify_password_reset(data['verification_key'], data['password'])
#             return response.py.ok(result)
#         except IMException as e:
#             return response.py.error(e.args[0])
