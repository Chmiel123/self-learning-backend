from src.logic import course_logic
from src.models.content.category import Category
from src.models.content.category_course_link import CategoryCourseLink
from src.models.content.course import Course
from src.models.system.entity_status import EntityStatus
from src.test.base_with_context_test import BaseWithContextTest
from src.utils.exceptions import CategoryCantAddCoursesException, NotAuthorizedException, CourseIdNotFoundException


class CourseLogicTest(BaseWithContextTest):
    def setUp(self):
        super().setUp()
        category1 = Category()
        category1.name = 'a'
        category1.content = 'a is a category'
        category1.language_id = 1
        category1.can_add_courses = True
        category1.save_to_db()
        category2 = Category()
        category2.name = 'b'
        category2.content = 'b is a category'
        category2.language_id = 1
        category2.can_add_courses = False
        category2.save_to_db()

    def test_create_course(self):
        course_logic.create_or_update({
            "id": None,
            "category_ids": [
                1
            ],
            "content": "New course description.",
            "language_id": 1,
            "name": "New course",
            "status": 1
        })
        course = Course.find_by_id(1)
        self.assertEqual(1, course.id)
        self.assertEqual("New course", course.name)
        link = CategoryCourseLink.find_by_category_id_course_id(1, 1)
        self.assertIsNotNone(link)

    def test_create_course_on_cant_add_courses_category(self):
        self.assertRaises(CategoryCantAddCoursesException,
                          course_logic.create_or_update, {
                              "id": None,
                              "category_ids": [
                                  2
                              ],
                              "content": "New course description.",
                              "language_id": 1,
                              "name": "New course",
                              "status": 1
                          })

    def test_create_update_course(self):
        course_logic.create_or_update({
            "id": None,
            "category_ids": [
                1
            ],
            "content": "New course description.",
            "language_id": 1,
            "name": "New course",
            "status": 2
        })
        course = Course.find_by_id(1)
        self.assertEqual(1, course.id)
        self.assertEqual("New course", course.name)
        self.assertEqual(EntityStatus.draft, course.status)
        link = CategoryCourseLink.find_by_category_id_course_id(1, 1)
        self.assertIsNotNone(link)
        course_logic.create_or_update({
            "id": course.id,
            "category_ids": [
                1
            ],
            "content": "New course description. Edited",
            "language_id": 1,
            "name": "New course edited",
            "status": 2
        })
        course = Course.find_by_id(1)
        self.assertEqual(1, course.id)
        self.assertEqual("New course edited", course.name)
        self.assertEqual(EntityStatus.active, course.status)

    def test_get_course(self):
        course_logic.create_or_update({
            "id": None,
            "category_ids": [
                1
            ],
            "content": "New course description.",
            "language_id": 1,
            "name": "New course",
            "status": 1
        })
        result = course_logic.get_course_by_id(1)
        self.assertEqual(1, result['id'])
        self.assertEqual("New course", result['name'])
        self.assertEqual(1, result['category_ids'][0])

    def test_get_courses_for_category(self):
        course_logic.create_or_update({
            "id": None,
            "category_ids": [
                1
            ],
            "content": "New course description.",
            "language_id": 1,
            "name": "New course 1",
            "status": 1
        })
        course_logic.create_or_update({
            "id": None,
            "category_ids": [
                1
            ],
            "content": "New course description.",
            "language_id": 1,
            "name": "New course 2",
            "status": 1
        })
        result = course_logic.get_courses_for_category(1, 1, 100)
        self.assertEqual(1, result['courses'][0]['id'])
        self.assertEqual("New course 1", result['courses'][0]['name'])
        self.assertEqual(2, result['courses'][1]['id'])
        self.assertEqual("New course 2", result['courses'][1]['name'])

    def test_delete(self):
        course_logic.create_or_update({
            "id": None,
            "category_ids": [
                1
            ],
            "content": "New course description.",
            "language_id": 1,
            "name": "New course 1",
            "status": 1
        })
        course_logic.delete(1)
        course = Course.find_by_id(1)
        self.assertEqual(EntityStatus.deleted, course.status)
        course_logic.delete(1)
        course = Course.find_by_id(1)
        self.assertEqual(EntityStatus.deleted, course.status)

    def test_move_to_another_category(self):
        category = Category()
        category.name = 'c'
        category.content = 'c is a category'
        category.language_id = 1
        category.can_add_courses = True
        category.save_to_db()
        course_logic.create_or_update({
            "id": None,
            "category_ids": [
                1
            ],
            "content": "New course description.",
            "language_id": 1,
            "name": "New course 1",
            "status": 1
        })
        result = course_logic.get_course_by_id(1)
        self.assertEqual(1, result['category_ids'][0])
        course_logic.create_or_update({
            "id": 1,
            "category_ids": [
                3
            ],
            "content": "New course description.",
            "language_id": 1,
            "name": "New course 1",
            "status": 1
        })
        result = course_logic.get_course_by_id(1)
        self.assertEqual(3, result['category_ids'][0])

    def test_number_active_courses_int_category(self):
        category = Category()
        category.name = 'c'
        category.content = 'c is a category'
        category.language_id = 1
        category.can_add_courses = True
        category.save_to_db()
        category = Category.find_by_id(1)
        self.assertEqual(0, category.nr_active_courses)
        course_logic.create_or_update({
            "id": None,
            "category_ids": [
                1
            ],
            "content": "New course description.",
            "language_id": 1,
            "name": "New course 1",
            "status": 1
        })
        course_logic.create_or_update({
            "id": 1,
            "category_ids": [
                1
            ],
            "content": "New course description.",
            "language_id": 1,
            "name": "New course 1",
            "status": 2
        })
        category = Category.find_by_id(1)
        self.assertEqual(1, category.nr_active_courses)
        course_logic.create_or_update({
            "id": None,
            "category_ids": [
                1
            ],
            "content": "New course description.",
            "language_id": 1,
            "name": "New course 2",
            "status": 1
        })
        course_logic.create_or_update({
            "id": 2,
            "category_ids": [
                1, 3
            ],
            "content": "New course description.",
            "language_id": 1,
            "name": "New course 2",
            "status": 2
        })
        category = Category.find_by_id(1)
        self.assertEqual(2, category.nr_active_courses)
        course_logic.create_or_update({
            "id": 2,
            "category_ids": [
                1
            ],
            "content": "New course description.",
            "language_id": 1,
            "name": "New course 2",
            "status": 3
        })
        category = Category.find_by_id(1)
        self.assertEqual(1, category.nr_active_courses)
        course_logic.delete(1)
        category = Category.find_by_id(1)
        self.assertEqual(0, category.nr_active_courses)

    def test_not_authorized_to_update(self):
        course_logic.create_or_update({
            "id": None,
            "category_ids": [
                1
            ],
            "content": "New course description.",
            "language_id": 1,
            "name": "New course",
            "status": 2
        })
        self.login_as_user()
        self.assertRaises(NotAuthorizedException,
                          course_logic.create_or_update, {
                                "id": 1,
                                "category_ids": [
                                    1
                                ],
                                "content": "New course description. Edited",
                                "language_id": 1,
                                "name": "New course edited",
                                "status": 2
                            })
        self.assertRaises(NotAuthorizedException, course_logic.delete, 1)

    def test_id_not_found(self):
        course_logic.create_or_update({
            "id": None,
            "category_ids": [
                1
            ],
            "content": "New course description.",
            "language_id": 1,
            "name": "New course",
            "status": 2
        })
        self.assertRaises(CourseIdNotFoundException,
                          course_logic.create_or_update, {
                                "id": 2,
                                "category_ids": [
                                    1
                                ],
                                "content": "New course description. Edited",
                                "language_id": 1,
                                "name": "New course edited",
                                "status": 2
                            })
        self.assertRaises(CourseIdNotFoundException, course_logic.delete, 3)
