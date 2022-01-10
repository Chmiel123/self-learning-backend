from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from src.logic import lesson_logic
from src.utils import assert_type_nullable, assert_type
from src.utils.response import ok

lesson_get_parser = reqparse.RequestParser()
lesson_get_parser.add_argument('lesson_id', location='args', type=int, required=False)
lesson_get_parser.add_argument('course_id', location='args', type=int, required=False)

lesson_post_parser = reqparse.RequestParser()
lesson_post_parser.add_argument('lesson', type=dict, help='This field cannot be blank', required=True)

lesson_delete_parser = reqparse.RequestParser()
lesson_delete_parser.add_argument('id', type=int, help='This field cannot be blank', required=True)


class LessonResource(Resource):
    def get(self):
        """Get lesson detail or lessons for course
        ---
        tags:
          - Content
        parameters:
          - name: lesson_id
            type: int
            in: query
            default: 1
          - name: course_id
            type: int
            in: query
            default: 1
        responses:
          200:
            description: OK.
        """
        data = lesson_get_parser.parse_args()
        result = {}
        if data['lesson_id']:
            result = lesson_logic.get_lesson_by_id(data['lesson_id'])
            return ok(result)
        if data['course_id']:
            result = lesson_logic.get_lessons_for_course(data['course_id'])
        return ok(result)

    @jwt_required()
    def post(self):
        """Create or Update a lesson
        ---
        tags:
          - Content
        parameters:
          - name: body
            in: body
            required: true
            schema:
              properties:
                lesson:
                  type: object
                  properties:
                      id:
                        type: int
                        example: null
                      course_id:
                        type: int
                        example: 2
                      type:
                        type: string
                        enum: [1, 2, 3]
                        example: 1
                      order:
                        type: int
                        example: 0
                      name:
                        type: string
                        example: New lesson
                      content:
                        type: string
                        example: New lesson content.
                      status:
                        type: string
                        enum: [1, 2, 3]
                        example: 1
                      language_id:
                        type: int
                        example: 37
        responses:
          200:
            description: OK.
        """
        data = lesson_post_parser.parse_args()
        result = None
        if data['lesson']:
            assert_type_nullable(data['lesson']['id'], int)
            assert_type(data['lesson']['course_id'], int)
            assert_type(data['lesson']['type'], int)
            assert_type(data['lesson']['order'], int)
            assert_type(data['lesson']['name'], str)
            assert_type(data['lesson']['content'], str)
            assert_type(data['lesson']['status'], int)
            assert_type(data['lesson']['language_id'], int)
            result = lesson_logic.create_or_update(data['lesson'])
        return ok(result)

    @jwt_required()
    def delete(self):
        """Delete a lesson
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
        data = lesson_delete_parser.parse_args()
        result = lesson_logic.delete(data['id'])
        return ok(result)
