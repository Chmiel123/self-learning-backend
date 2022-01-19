from src.logic import test_logic, premium_logic, lesson_logic
from src.models import Category, Course, Lesson
from src.models.content.category_course_link import CategoryCourseLink
from src.models.content.question import Question
from src.models.content.test import Test
from src.models.system.entity_status import EntityStatus
from src.models.system.lesson_type import LessonType
from src.models.system.test_status import TestStatus
from src.test.base_with_context_test import BaseWithContextTest
from src.utils.exceptions import TestNotFoundException, TestNotValidException

questions = [
    ['Question 01', "['A','B','C','D']", "[3]", 1, 2, "Solution"],
    ['Question 02', "['A','B','C','D']", "[3]", 1, 2, "Solution"],
    ['Question 03', "['A','B','C','D']", "[3]", 1, 2, "Solution"],
    ['Question 04', "['A','B','C','D']", "[3]", 1, 2, "Solution"],
    ['Question 05', "['A','B','C','D']", "[3]", 1, 2, "Solution"],
    ['Question 06', "['A','B','C','D']", "[3]", 1, 2, "Solution"],
    ['Question 07', "['1','2','3','4']", "[1]", 3, 3, "Solution"],
    ['Question 08', "['1','2','3','4']", "[2]", 4, 4, "Solution"]
]


invalid_questions = [
    ['Question 01', "['A','B','C','D']", "[3]", 1, 2, "Solution"],
    ['Question 02', "['A','B','C','D']", "[3]", 1, 2, "Solution"],
    ['Question 03', "['A','B','C','D']", "[3]", 1, 3, "Solution"]
]


class TestLogicTest(BaseWithContextTest):
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
        lesson = Lesson()
        lesson.name = 'c'
        lesson.content = 'c is a lesson'
        lesson.language_id = 1
        lesson.author_id = 1
        lesson.course_id = course1.id
        lesson.type = LessonType.test
        lesson.duration_minutes = 60
        lesson.save_to_db()
        for q in questions:
            question = Question()
            question.lesson_id = lesson.id
            question.question = q[0]
            question.available_answers = q[1]
            question.correct_answers = q[2]
            question.order_begin = q[3]
            question.order_end = q[4]
            question.solution = q[5]
            question.save_to_db()

    def test_generate_test(self):
        self.c = self.app.test_request_context()
        self.c.push()
        headers = {
        }
        self.c.request.headers = headers
        test = test_logic.generate_test(1)
        self.assertEqual("['A','B','C','D']", test['questions'][0]['available_answers'])
        self.assertEqual("['A','B','C','D']", test['questions'][1]['available_answers'])
        self.assertRaises(KeyError, lambda: test['questions'][0]['correct_answers'])
        self.assertRaises(KeyError, lambda: test['questions'][0]['solution'])
        self.assertEqual('Question 07', test['questions'][2]['question'])
        self.assertEqual('Question 08', test['questions'][3]['question'])

    def test_generate_test_save_to_db_if_premium(self):
        test_logic.generate_test(1)
        tests = Test.find_by_lesson_id_and_account_id(1, 1)
        self.assertEqual(0, len(tests))
        premium_logic.add_premium(1)
        test_logic.generate_test(1)
        test = Test.find_by_lesson_id_and_account_id(1, 1)[0]
        self.assertEqual(TestStatus.in_progress, test.status)

    def test_get_test(self):
        premium_logic.add_premium(1)
        test_logic.generate_test(1)
        result = test_logic.get_tests(1)
        self.assertEqual(1, result['tests'][0]['lesson_id'])
        self.assertEqual(1, result['tests'][0]['account_id'])

    def test_test_not_found(self):
        self.assertRaises(TestNotFoundException, test_logic.generate_test, 2)

    def test_invalid_test(self):
        lesson = Lesson()
        lesson.name = 'd'
        lesson.content = 'd is a lesson'
        lesson.language_id = 1
        lesson.author_id = 1
        lesson.course_id = 1
        lesson.type = LessonType.test
        lesson.is_valid_test = False
        lesson.save_to_db()
        for q in invalid_questions:
            question = Question()
            question.lesson_id = lesson.id
            question.question = q[0]
            question.available_answers = q[1]
            question.correct_answers = q[2]
            question.order_begin = q[3]
            question.order_end = q[4]
            question.solution = q[5]
            question.save_to_db()
        self.assertRaises(TestNotValidException, test_logic.generate_test, 2)
