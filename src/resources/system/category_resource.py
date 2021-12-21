from flask_restful import Resource, reqparse

from src.logic import category_logic
from src.models.system.category import Category
from src.models.system.language import Language
from src.utils.response import ok


category_get_parser = reqparse.RequestParser()
category_get_parser.add_argument('language', location='args', required=True)


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
        if data['language']:
            result = category_logic.get_all_categories_for_language(data['language'])
        return ok(result)

