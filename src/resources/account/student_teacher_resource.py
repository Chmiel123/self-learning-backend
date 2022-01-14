from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from src.logic import student_teacher_logic
from src.utils.response import ok


parser = reqparse.RequestParser()
parser.add_argument('teacher_id', type=int, help='This field cannot be blank', required=True)
parser.add_argument('student_id', type=int, help='This field cannot be blank', required=True)


class StudentTeacherLink(Resource):
    @jwt_required()
    def get(self):
        """Get teachers and students of the current account
        ---
        tags:
          - Account
        responses:
          200:
            description: OK.
        """
        result = student_teacher_logic.get_details()
        return ok(result)

    @jwt_required()
    def post(self):
        """Request or confirm a new teacher student link
        ---
        tags:
          - Account
        parameters:
          - name: body
            in: body
            required: true
            schema:
              properties:
                teacher_id:
                  type: int
                  example: 1
                student_id:
                  type: int
                  example: 2
        responses:
          200:
            description: OK.
        """
        data = parser.parse_args()
        student_teacher_logic.make_request(data['teacher_id'], data['student_id'])
        return ok()

    @jwt_required()
    def delete(self):
        """Deletes a student teacher link or request
        ---
        tags:
          - Account
        parameters:
          - name: body
            in: body
            required: true
            schema:
              properties:
                teacher_id:
                  type: int
                  example: 1
                student_id:
                  type: int
                  example: 2
        responses:
          200:
            description: OK.
        """
        data = parser.parse_args()
        student_teacher_logic.remove_request_and_link(data['teacher_id'], data['student_id'])
        return ok()
