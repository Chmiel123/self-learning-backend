from typing import List

from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from src.logic import course_logic
from src.services import services
from src.utils import assert_type_nullable, assert_type
from src.utils.response import ok

course_get_parser = reqparse.RequestParser()
course_get_parser.add_argument('course_id', location='args', type=int, required=False)
course_get_parser.add_argument('category_id', location='args', type=int, required=False)
course_get_parser.add_argument('page_number', location='args', type=int, required=False)
course_get_parser.add_argument('page_size', location='args', type=int, required=False)

course_post_parser = reqparse.RequestParser()
course_post_parser.add_argument('course', type=dict, help='This field cannot be blank', required=True)

course_delete_parser = reqparse.RequestParser()
course_delete_parser.add_argument('id', type=int, help='This field cannot be blank', required=True)


class CourseResource(Resource):
    def get(self):
        """Get courses for category
        ---
        tags:
          - Content
        parameters:
          - name: course_id
            type: int
            in: query
            default: null
          - name: category_id
            type: int
            in: query
            default: 1
          - name: page_number
            type: int
            in: query
            default: 1
          - name: page_size
            type: int
            in: query
            default: 100
        responses:
          200:
            description: OK.
        """
        data = course_get_parser.parse_args()
        result = {}
        if data['course_id']:
            result = course_logic.get_course_by_id(data['course_id'])
            return ok(result)
        page_number = 1
        if data['page_number']:
            page_number = data['page_number']
        page_size = services.flask.config['DEFAULT_PAGE_SIZE']
        if data['page_size']:
            page_size = data['page_size']
        if data['category_id']:
            result = course_logic.get_courses_for_category(data['category_id'], page_number, page_size)
        return ok(result)

    @jwt_required()
    def post(self):
        """Create or Update a course
        ---
        tags:
          - Content
        parameters:
          - name: body
            in: body
            required: true
            schema:
              properties:
                course:
                  type: object
                  properties:
                      id:
                        type: int
                        example: null
                      category_ids:
                        type: array
                        example: [5, 7]
                      name:
                        type: string
                        example: New course
                      content:
                        type: string
                        example: New course description.
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
        data = course_post_parser.parse_args()
        result = None
        if data['course']:
            assert_type_nullable(data['course']['id'], int)
            assert_type(data['course']['category_ids'], list)
            assert_type(data['course']['name'], str)
            assert_type(data['course']['content'], str)
            assert_type(data['course']['status'], int)
            assert_type(data['course']['language_id'], int)
            result = course_logic.create_or_update(data['course'])
        return ok(result)

    @jwt_required()
    def delete(self):
        """Delete a course
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
        data = course_delete_parser.parse_args()
        result = course_logic.delete(data['id'])
        return ok(result)
