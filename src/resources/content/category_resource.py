from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse

from src.logic import category_logic
from src.utils.response import ok

category_get_parser = reqparse.RequestParser()
category_get_parser.add_argument('language', location='args', required=True)

category_post_parser = reqparse.RequestParser()
category_post_parser.add_argument('category', type=dict, help='This field cannot be blank', required=True)

category_delete_parser = reqparse.RequestParser()
category_delete_parser.add_argument('id', type=int, help='This field cannot be blank', required=True)


class CategoryResource(Resource):
    def get(self):
        """Get all categories details
        ---
        tags:
          - Content
        parameters:
          - name: language
            type: string
            in: query
            default: en
        responses:
          200:
            description: OK.
        """
        data = category_get_parser.parse_args()
        result = {}
        if data['language']:
            result = category_logic.get_all_categories_for_language(data['language'])
        return ok(result)

    @jwt_required()
    def post(self):
        """Create or Update a category
        ---
        tags:
          - Content
        parameters:
          - name: body
            in: body
            required: true
            schema:
              properties:
                category:
                  type: object
                  properties:
                      id:
                        type: int
                        example: null
                      parent_id:
                        type: int
                        example: null
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
                      can_add_lesson_groups:
                        type: bool
                        example: true
        responses:
          200:
            description: OK.
        """
        data = category_post_parser.parse_args()
        result = None
        if data['category']:
            result = category_logic.create_or_update(data['category'])
        return ok(result)

    @jwt_required()
    def delete(self):
        """Delete a category
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
        data = category_delete_parser.parse_args()
        result = category_logic.delete(data['id'])
        return ok(result)
