from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from src.logic import admin_privilege_logic
from src.utils.response import ok

admin_privilege_get_parser = reqparse.RequestParser()
admin_privilege_get_parser.add_argument('account_id', location='args', type=int, required=False)

admin_privilege_post_parser = reqparse.RequestParser()
admin_privilege_post_parser.add_argument('admin_privilege', type=dict, help='This field cannot be blank', required=True)

admin_privilege_delete_parser = reqparse.RequestParser()
admin_privilege_delete_parser.add_argument('id', type=int, help='This field cannot be blank', required=True)


class AdminPrivilegeResource(Resource):
    def get(self):
        """Get admin privilege detail for an account
        ---
        tags:
          - Content
        parameters:
          - name: account_id
            type: int
            in: query
            default: 1
        responses:
          200:
            description: OK.
        """
        data = admin_privilege_get_parser.parse_args()
        result = {}
        if data['account_id']:
            result = admin_privilege_logic.get_admin_privileges_for_account(data['account_id'])
        return ok(result)

    @jwt_required()
    def post(self):
        """Create or Update an admin privilege
        ---
        tags:
          - Content
        parameters:
          - name: body
            in: body
            required: true
            schema:
              properties:
                admin_privilege:
                  type: object
                  properties:
                      account_id:
                        type: int
                        example: 1
                      language_id:
                        type: int
                        example: 37
                      strength:
                        type: int
                        example: 1
        responses:
          200:
            description: OK.
        """
        data = admin_privilege_post_parser.parse_args()
        result = None
        if data['admin_privilege']:
            result = admin_privilege_logic.create_or_update(data['admin_privilege'])
        return ok(result)

    @jwt_required()
    def delete(self):
        """Delete an admin privilege
        ---
        tags:
          - Content
        parameters:
          - name: body
            in: body
            required: true
            schema:
              properties:
                admin_privilege:
                  type: object
                  properties:
                      account_id:
                        type: int
                        example: 1
                      language_id:
                        type: int
                        example: 37
        responses:
          200:
            description: OK.
        """
        data = admin_privilege_delete_parser.parse_args()
        result = admin_privilege_logic.delete(data['admin_privilege'])
        return ok(result)
