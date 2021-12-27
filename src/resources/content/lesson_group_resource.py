from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from src.logic import lesson_group_logic
from src.services import services
from src.utils.response import ok

lesson_group_get_parser = reqparse.RequestParser()
lesson_group_get_parser.add_argument('category_id', location='args', type=int, required=True)
lesson_group_get_parser.add_argument('page_number', location='args', type=int, required=False)
lesson_group_get_parser.add_argument('page_size', location='args', type=int, required=False)

lesson_group_post_parser = reqparse.RequestParser()
lesson_group_post_parser.add_argument('lesson_group', type=dict, help='This field cannot be blank', required=True)

lesson_group_delete_parser = reqparse.RequestParser()
lesson_group_delete_parser.add_argument('id', type=int, help='This field cannot be blank', required=True)


class LessonGroupResource(Resource):
    def get(self):
        """Get lesson groups for category
        ---
        tags:
          - Content
        parameters:
          - name: category_id
            type: int
            in: query
            default: 1
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
        data = lesson_group_get_parser.parse_args()
        page_number = 1
        if data['page_number']:
            page_number = data['page_number']
        page_size = services.flask.config['DEFAULT_PAGE_SIZE']
        if data['page_size']:
            page_size = data['page_size']
        result = {}

        if data['category_id']:
            result = lesson_group_logic.get_lesson_groups_for_category(data['category_id'], page_number, page_size)
        return ok(result)

    @jwt_required()
    def post(self):
        """Create or Update a lesson group
        ---
        tags:
          - Content
        parameters:
          - name: body
            in: body
            required: true
            schema:
              properties:
                lesson_group:
                  type: object
                  properties:
                      id:
                        type: int
                        example: null
                      category_id:
                        type: int
                        example: 1
                      name:
                        type: string
                        example: New category
                      content:
                        type: string
                        example: New category description.
                      status:
                        type: string
                        enum: [1, 2, 3]
                        example: 1
                      language_id:
                        type: int
                        example: 57
        responses:
          200:
            description: OK.
        """
        data = lesson_group_post_parser.parse_args()
        result = None
        if data['lesson_group']:
            result = lesson_group_logic.create_or_update(data['lesson_group'])
        return ok(result)

    @jwt_required()
    def delete(self):
        """Delete a lesson group
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
        data = lesson_group_delete_parser.parse_args()
        result = lesson_group_logic.delete(data['id'])
        return ok(result)
