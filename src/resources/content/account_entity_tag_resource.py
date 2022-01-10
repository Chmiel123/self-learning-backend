from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from src.logic import account_entity_tag_logic
from src.utils.response import ok

account_entity_tag_get_parser = reqparse.RequestParser()
account_entity_tag_get_parser.add_argument('entity_id_range', location='args', type=str, required=True)
account_entity_tag_get_parser.add_argument('entity_type', location='args', type=int, required=True)

account_entity_tag_post_parser = reqparse.RequestParser()
account_entity_tag_post_parser.add_argument('account_entity_tag', type=dict, help='This field cannot be blank',
                                            required=True)

account_entity_tag_delete_parser = reqparse.RequestParser()
account_entity_tag_delete_parser.add_argument('account_entity_tag', type=dict, help='This field cannot be blank',
                                              required=True)


class AccountEntityTagResource(Resource):
    @jwt_required()
    def get(self):
        """Get account entity tag detail for entity
        ---
        tags:
          - Content
        parameters:
          - name: entity_id_range
            type: string
            in: query
            default: 1-100
          - name: entity_type
            type: int
            in: query
            default: 1
        responses:
          200:
            description: OK.
        """
        data = account_entity_tag_get_parser.parse_args()
        result = {}
        if data['entity_id_range'] and data['entity_type']:
            result = account_entity_tag_logic.get_account_entity_tags_for_entities(data['entity_id_range'],
                                                                                   data['entity_type'])
        return ok(result)

    @jwt_required()
    def post(self):
        """Create or update an account entity tag
        ---
        tags:
          - Content
        parameters:
          - name: body
            in: body
            required: true
            schema:
              properties:
                account_entity_tag:
                  type: object
                  properties:
                      entity_id:
                        type: int
                        example: 1
                      entity_type:
                        type: string
                        enum: [1, 2, 3, 4, 5]
                        example: 1
                      like:
                        type: bool
                        example: False
                      dislike:
                        type: bool
                        example: True
                      favorite:
                        type: bool
                        example: True
                      in_progress:
                        type: bool
                        example: False
                      completed:
                        type: bool
                        example: False
        responses:
          200:
            description: OK.
        """
        data = account_entity_tag_post_parser.parse_args()
        result = None
        if data['account_entity_tag']:
            result = account_entity_tag_logic.create_or_update(data['account_entity_tag'])
        return ok(result)

    @jwt_required()
    def delete(self):
        """Delete an account entity tag
        ---
        tags:
          - Content
        parameters:
          - name: body
            in: body
            required: true
            schema:
              properties:
                account_entity_tag:
                  type: object
                  properties:
                      entity_id:
                        type: int
                        example: 1
                      entity_type:
                        type: string
                        enum: [1, 2, 3, 4, 5]
                        example: 1
        responses:
          200:
            description: OK.
        """
        data = account_entity_tag_delete_parser.parse_args()
        result = account_entity_tag_logic.delete(data['account_entity_tag'])
        return ok(result)
