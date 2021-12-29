from flask_restful import Resource

from src.models.system.entity_status import EntityStatus
from src.models.system.entity_type import EntityType
from src.models.system.language import Language
from src.models.system.lesson_type import LessonType
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


class EnumResource(Resource):
    def get(self):
        """Get all enum details
        ---
        tags:
          - System
        responses:
          200:
            description: OK.
        """
        return ok({
            'entity_status': {x.name: x.value for x in EntityStatus},
            'entity_type': {x.name: x.value for x in EntityType},
            'lesson_type': {x.name: x.value for x in LessonType}
        })
