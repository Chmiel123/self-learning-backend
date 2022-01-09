from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from src.logic import comment_logic
from src.services import services
from src.utils.response import ok

comment_get_parser = reqparse.RequestParser()
comment_get_parser.add_argument('parent_id', location='args', type=str, required=True)
comment_get_parser.add_argument('parent_type', location='args', type=int, required=True)
comment_get_parser.add_argument('page_number', location='args', type=int, required=False)
comment_get_parser.add_argument('page_size', location='args', type=int, required=False)

comment_post_parser = reqparse.RequestParser()
comment_post_parser.add_argument('comment', type=dict, help='This field cannot be blank', required=True)

comment_delete_parser = reqparse.RequestParser()
comment_delete_parser.add_argument('id', type=int, help='This field cannot be blank', required=True)


class CommentResource(Resource):
    def get(self):
        """Get comment detail or comments for lesson
        ---
        tags:
          - Content
        parameters:
          - name: parent_id
            type: string
            in: query
            default: 1
          - name: parent_type
            type: int
            in: query
            default: 2
          - name: page_number
            type: int
            in: query
            default: 1
          - name: page_size
            type: int
            in: query
            default: 100
        responses:
          200:
            description: OK.
        """
        data = comment_get_parser.parse_args()

        page_number = 1
        if data['page_number']:
            page_number = data['page_number']

        page_size = services.flask.config['DEFAULT_PAGE_SIZE']
        if data['page_size']:
            page_size = data['page_size']

        result = {}
        if data['parent_id'] and data['parent_type']:
            result = comment_logic.get_comments_for_parent(data['parent_id'], data['parent_type'],
                                                           page_number, page_size)
        return ok(result)

    @jwt_required()
    def post(self):
        """Create or Update a comment
        ---
        tags:
          - Content
        parameters:
          - name: body
            in: body
            required: true
            schema:
              properties:
                comment:
                  type: object
                  properties:
                      id:
                        type: int
                        example: null
                      parent_id:
                        type: int
                        example: 1
                      parent_type:
                        type: string
                        enum: [1, 2, 3, 4, 5]
                        example: 2
                      content:
                        type: string
                        example: This is a comment
        responses:
          200:
            description: OK.
        """
        data = comment_post_parser.parse_args()
        result = None
        if data['comment']:
            result = comment_logic.create_or_update(data['comment'])
        return ok(result)

    @jwt_required()
    def delete(self):
        """Delete a comment
        ---
        tags:
          - Content
        parameters:
          - name: body
            in: body
            required: true
            schema:
              properties:
                id:
                  type: int
                  example: 1
        responses:
          200:
            description: OK.
        """
        data = comment_delete_parser.parse_args()
        result = comment_logic.delete(data['id'])
        return ok(result)
