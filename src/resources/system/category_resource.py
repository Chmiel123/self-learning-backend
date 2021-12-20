from flask_restful import Resource, reqparse

from src.models.system.category import Category
from src.utils.response import ok


class CategoryResource(Resource):
    def get(self):
        """Get all categories details
        ---
        tags:
          - System
        responses:
          200:
            description: OK.
        """
        categories = Category.find_all()
        return ok({
            'categories': [x.serialize() for x in categories]
        })

