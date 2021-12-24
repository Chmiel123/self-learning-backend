from flask_restful import Resource

from src.models.system.language import Language
from src.utils.response import ok


class LanguageResource(Resource):
    def get(self):
        """Get all language details
        ---
        tags:
          - System
        responses:
          200:
            description: OK.
        """
        result = [x.serialize() for x in Language.find_all()]
        return ok(result)
