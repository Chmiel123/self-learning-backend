from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from src.logic import question_logic, answer_logic
from src.utils import assert_type_nullable, assert_type
from src.utils.response import ok

answer_get_parser = reqparse.RequestParser()
answer_get_parser.add_argument('test_id', location='args', type=int, required=True)

answer_post_parser = reqparse.RequestParser()
answer_post_parser.add_argument('answer', type=dict, help='This field cannot be blank', required=True)


class AnswerResource(Resource):
    @jwt_required()
    def get(self):
        """Get questions detail for a test
        ---
        tags:
          - Content
        parameters:
          - name: test_id
            type: int
            in: query
            default: 1
        responses:
          200:
            description: OK.
        """
        data = answer_get_parser.parse_args()
        result = {}
        if data['test_id']:
            result = answer_logic.get_answers_for_test(data['test_id'])
        return ok(result)

    @jwt_required()
    def post(self):
        """Create or Update an answer
        ---
        tags:
          - Content
        parameters:
          - name: body
            in: body
            required: true
            schema:
              properties:
                answer:
                  type: object
                  properties:
                      id:
                        type: int
                        example: 1
                      student_answer:
                        type: string
                        example: B
                      teacher_remark:
                        type: string
                        example:
                      points_earned:
                        type: number
                        example: 1.0
        responses:
          200:
            description: OK.
        """
        data = answer_post_parser.parse_args()
        result = None
        if data['answer']:
            assert_type(data['answer']['id'], int)
            assert_type_nullable(data['answer']['student_answer'], str)
            assert_type_nullable(data['answer']['teacher_remark'], str)
            assert_type_nullable(data['answer']['points_earned'], float)
            result = answer_logic.update(data['question'])
        return ok(result)
