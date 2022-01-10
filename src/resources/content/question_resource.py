from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from src.logic import question_logic
from src.utils import assert_type_nullable, assert_type
from src.utils.response import ok

question_get_parser = reqparse.RequestParser()
question_get_parser.add_argument('lesson_id', location='args', type=int, required=True)

question_post_parser = reqparse.RequestParser()
question_post_parser.add_argument('question', type=dict, help='This field cannot be blank', required=True)

question_delete_parser = reqparse.RequestParser()
question_delete_parser.add_argument('id', type=int, help='This field cannot be blank', required=True)


class QuestionResource(Resource):
    def get(self):
        """Get question detail or questions for lesson
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
        data = question_get_parser.parse_args()
        result = {}
        if data['lesson_id']:
            result = question_logic.get_questions_for_lesson(data['lesson_id'])
        return ok(result)

    @jwt_required()
    def post(self):
        """Create or Update a question
        ---
        tags:
          - Content
        parameters:
          - name: body
            in: body
            required: true
            schema:
              properties:
                question:
                  type: object
                  properties:
                      id:
                        type: int
                        example: null
                      lesson_id:
                        type: int
                        example: 2
                      order_begin:
                        type: int
                        example: 1
                      order_end:
                        type: int
                        example: 1
                      question:
                        type: string
                        example: How much is 2 + 2?
                      available_answers:
                        type: array
                        example: ['A', 'B', 'C', 'D']
                      correct_answers:
                        type: array
                        example: ['C']
                      solution:
                        type: string
                        example: ""
        responses:
          200:
            description: OK.
        """
        data = question_post_parser.parse_args()
        result = None
        if data['question']:
            assert_type_nullable(data['question']['id'], int)
            assert_type(data['question']['lesson_id'], int)
            assert_type(data['question']['order_begin'], int)
            assert_type(data['question']['order_end'], int)
            assert_type(data['question']['question'], str)
            assert_type(data['question']['available_answers'], list)
            assert_type(data['question']['correct_answers'], list)
            assert_type(data['question']['solution'], str)
            result = question_logic.create_or_update(data['question'])
        return ok(result)

    @jwt_required()
    def delete(self):
        """Delete a question
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
        data = question_delete_parser.parse_args()
        result = question_logic.delete(data['id'])
        return ok(result)
