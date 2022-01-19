from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from src.logic import test_logic
from src.utils.response import ok

test_get_parser = reqparse.RequestParser()
test_get_parser.add_argument('lesson_id', type=int, help='This field cannot be blank', required=True)


class GenerateTestResource(Resource):
    def get(self):
        """Get generated test for a lesson, if user logged in and has premium time the test is saved on the server.
        ---
        tags:
          - Content
        parameters:
          - name: lesson_id
            type: int
            in: query
            default: 1
        responses:
          200:
            description: OK.
        """
        data = test_get_parser.parse_args()
        result = {}
        if data['lesson_id']:
            result = test_logic.generate_test(data['lesson_id'])
        return ok(result)


class TestResource(Resource):
    @jwt_required()
    def get(self):
        """Get tests for a lesson.
        ---
        tags:
          - Content
        parameters:
          - name: lesson_id
            type: int
            in: query
            default: 1
        responses:
          200:
            description: OK.
        """
        data = test_get_parser.parse_args()
        result = {}
        if data['lesson_id']:
            result = test_logic.get_tests(data['lesson_id'])
        return ok(result)
