from flask_restful import Resource, reqparse

from src.logic import category_logic
from src.utils.response import ok

category_get_parser = reqparse.RequestParser()
category_get_parser.add_argument('language', location='args', required=True)

category_post_parser = reqparse.RequestParser()
category_post_parser.add_argument('category', type=dict, help='This field cannot be blank', required=True)


class CategoryResource(Resource):
    def get(self):
        """Get all categories details
        ---
        tags:
          - System
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

    def post(self):
        """Create or Update a category
        ---
        tags:
          - System
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
                      name:
                        type: string
                        example: New category
                      content:
                        type: string
                        example: New category description.
                      language:
                        type: string
                        example: en
        responses:
          200:
            description: OK.
        """
        data = category_post_parser.parse_args()
        if data['category']:
            category_logic.create_or_update(data['category'])
        return ok()