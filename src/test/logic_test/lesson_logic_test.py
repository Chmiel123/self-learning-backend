from src.logic import lesson_logic
from src.models.account.admin_privilege import AdminPrivilege
from src.models.content.category import Category
from src.models.content.category_course_link import CategoryCourseLink
from src.models.content.course import Course
from src.models.content.lesson import Lesson
from src.models.content.question import Question
from src.models.system.entity_status import EntityStatus
from src.models.system.language import Language
from src.models.system.lesson_type import LessonType
from src.test.base_with_context_test import BaseWithContextTest
from src.utils.exceptions import NotAuthorizedException, LessonIdNotFoundException, CourseIdNotFoundException, \
    LessonLanguageIdInvalidException


class LessonLogicTest(BaseWithContextTest):
    def setUp(self):
        super().setUp()
        category1 = Category()
        category1.name = 'a'
        category1.content = 'a is a category'
        category1.status = EntityStatus.active
        category1.language_id = 1
        category1.can_add_courses = True
        category1.author_id = 1
        category1.save_to_db()
        course1 = Course()
        course1.name = 'b'
        course1.content = 'b is a course'
        course1.status = EntityStatus.active
        course1.language_id = 1
        course1.author_id = 1
        course1.save_to_db()
        category_course_link = CategoryCourseLink()
        category_course_link.category_id = 1
        category_course_link.course_id = 1
        category_course_link.save_to_db()

    def test_create_lesson(self):
        lesson_logic.create_or_update({
            "id": None,
            "course_id": 1,
            "name": "New lesson",
            "content": "New lesson description.",
            "language_id": 1,
            "status": 1,
            "order": 2,
            "type": LessonType.lesson.value
        })
        lesson = Lesson.find_by_id(1)
        self.assertEqual(1, lesson.id)
        self.assertEqual("New lesson", lesson.name)
        self.assertEqual(LessonType.lesson, lesson.type)
        self.assertEqual(2, lesson.order)

    def test_create_update_lesson(self):
        lesson_logic.create_or_update({
            "id": None,
            "course_id": 1,
            "name": "New lesson",
            "content": "New lesson description.",
            "language_id": 1,
            "status": 1,
            "order": 2,
            "type": LessonType.lesson.value
        })
        lesson = Lesson.find_by_id(1)
        self.assertEqual(1, lesson.id)
        self.assertEqual("New lesson", lesson.name)
        self.assertEqual(LessonType.lesson, lesson.type)
        self.assertEqual(2, lesson.order)
        lesson_logic.create_or_update({
            "id": 1,
            "course_id": 1,
            "name": "New lesson 2",
            "content": "New lesson description.",
            "language_id": 1,
            "status": 2,
            "order": 3,
            "type": LessonType.test.value
        })
        lesson = Lesson.find_by_id(1)
        self.assertEqual(1, lesson.id)
        self.assertEqual("New lesson 2", lesson.name)
        self.assertEqual(LessonType.test, lesson.type)
        self.assertEqual(3, lesson.order)
        lesson_logic.create_or_update({
            "id": 1,
            "course_id": 1,
            "name": "New lesson 2",
            "content": "New lesson description.",
            "language_id": 1,
            "status": 2,
            "order": 3,
            "type": LessonType.test.value
        })
        lesson = Lesson.find_by_id(1)
        self.assertEqual(1, lesson.id)
        self.assertEqual("New lesson 2", lesson.name)
        self.assertEqual(LessonType.test, lesson.type)
        self.assertEqual(3, lesson.order)

    def test_get_lesson(self):
        lesson_logic.create_or_update({
            "id": None,
            "course_id": 1,
            "name": "New lesson",
            "content": "New lesson description.",
            "language_id": 1,
            "status": 1,
            "order": 2,
            "type": LessonType.lesson.value
        })
        result = lesson_logic.get_lesson_by_id(1)
        self.assertEqual(1, result['id'])
        self.assertEqual("New lesson", result['name'])
        self.assertEqual(1, result['status'])

    def test_get_lessons_for_course(self):
        lesson_logic.create_or_update({
            "id": None,
            "course_id": 1,
            "name": "New lesson 1",
            "content": "New lesson description.",
            "language_id": 1,
            "status": 1,
            "order": 2,
            "type": LessonType.lesson.value
        })
        lesson_logic.create_or_update({
            "id": None,
            "course_id": 1,
            "name": "New lesson 2",
            "content": "New lesson description.",
            "language_id": 1,
            "status": 1,
            "order": 3,
            "type": LessonType.lesson.value
        })
        result = lesson_logic.get_lessons_for_course(1)
        self.assertEqual(1, result['lessons'][0]['id'])
        self.assertEqual("New lesson 1", result['lessons'][0]['name'])
        self.assertEqual(2, result['lessons'][1]['id'])
        self.assertEqual("New lesson 2", result['lessons'][1]['name'])

    def test_delete(self):
        lesson_logic.create_or_update({
            "id": None,
            "course_id": 1,
            "name": "New lesson 1",
            "content": "New lesson description.",
            "language_id": 1,
            "status": 1,
            "order": 2,
            "type": LessonType.lesson.value
        })
        lesson_logic.delete(1)
        lesson = Lesson.find_by_id(1)
        self.assertEqual(EntityStatus.deleted, lesson.status)
        lesson_logic.delete(1)
        lesson = Lesson.find_by_id(1)
        self.assertEqual(EntityStatus.deleted, lesson.status)

    def test_not_authorized_to_update(self):
        lesson_logic.create_or_update({
            "id": None,
            "course_id": 1,
            "name": "New lesson 1",
            "content": "New lesson description.",
            "language_id": 1,
            "status": 1,
            "order": 2,
            "type": LessonType.lesson.value
        })
        self.login_as_user()
        self.assertRaises(NotAuthorizedException,
                          lesson_logic.create_or_update, {
                              "id": 1,
                              "course_id": 1,
                              "name": "New lesson 1",
                              "content": "New lesson description.",
                              "language_id": 1,
                              "status": 2,
                              "order": 2,
                              "type": LessonType.lesson.value
                          })
        self.assertRaises(NotAuthorizedException, lesson_logic.delete, 1)

    def test_id_not_found(self):
        self.assertRaises(LessonIdNotFoundException,
                          lesson_logic.create_or_update, {
                              "id": 2,
                              "course_id": 1,
                              "name": "New lesson 1",
                              "content": "New lesson description.",
                              "language_id": 1,
                              "status": 1,
                              "order": 2,
                              "type": LessonType.lesson.value
                          })
        self.assertRaises(LessonIdNotFoundException, lesson_logic.delete, 3)

    def test_parent_course_id_not_found(self):
        self.assertRaises(CourseIdNotFoundException,
                          lesson_logic.create_or_update, {
                              "id": None,
                              "course_id": 2,
                              "name": "New lesson 1",
                              "content": "New lesson description.",
                              "language_id": 1,
                              "status": 1,
                              "order": 2,
                              "type": LessonType.lesson.value
                          })

    def test_parent_course_different_langugage_id(self):
        language = Language()
        language.code = 'es'
        language.english_name = 'spanish'
        language.native_name = 'espanol'
        language.save_to_db()
        admin_privilege = AdminPrivilege()
        admin_privilege.account_id = 1
        admin_privilege.language_id = 2
        admin_privilege.strength = 5
        admin_privilege.save_to_db()
        self.assertRaises(LessonLanguageIdInvalidException,
                          lesson_logic.create_or_update, {
                              "id": None,
                              "course_id": 1,
                              "name": "New lesson 1",
                              "content": "New lesson description.",
                              "language_id": 2,
                              "status": 1,
                              "order": 2,
                              "type": LessonType.lesson.value
                          })

    def test_parent_course_different_user_id(self):
        self.login_as_user()
        self.assertRaises(NotAuthorizedException,
                          lesson_logic.create_or_update, {
                              "id": None,
                              "course_id": 1,
                              "name": "New lesson 1",
                              "content": "New lesson description.",
                              "language_id": 1,
                              "status": 1,
                              "order": 2,
                              "type": LessonType.lesson.value
                          })

    invalid_questions = [
        ['Question 01', "['A','B','C','D']", "[3]", 1, 2, "Solution"],
        ['Question 02', "['A','B','C','D']", "[3]", 1, 2, "Solution"],
        ['Question 03', "['A','B','C','D']", "[3]", 1, 3, "Solution"]
    ]

    def test_invalid_lesson_test(self):
        lesson = Lesson()
        lesson.name = 'c'
        lesson.content = 'c is a lesson'
        lesson.language_id = 1
        lesson.author_id = 1
        lesson.course_id = 1
        lesson.type = LessonType.test
        lesson.save_to_db()
        for q in LessonLogicTest.invalid_questions:
            question = Question()
            question.lesson_id = lesson.id
            question.question = q[0]
            question.available_answers = q[1]
            question.correct_answers = q[2]
            question.order_begin = q[3]
            question.order_end = q[4]
            question.solution = q[5]
            question.save_to_db()
        lesson_logic.create_or_update({
            "id": 1,
            "name": "c",
            "content": "c is a lesson",
            "status": 1,
            "order": 1,
            "language_id": 1,
            "type": LessonType.lesson.value
        })
        lesson = Lesson.find_by_id(1)
        self.assertEqual(False, lesson.is_valid_test)
