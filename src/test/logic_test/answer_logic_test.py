from datetime import datetime, timedelta

from src.logic import test_logic, premium_logic, lesson_logic, student_teacher_logic, answer_logic, account_logic
from src.models import Category, Course, Lesson
from src.models.content.answer import Answer
from src.models.content.category_course_link import CategoryCourseLink
from src.models.content.question import Question
from src.models.content.test import Test
from src.models.system.entity_status import EntityStatus
from src.models.system.lesson_type import LessonType
from src.models.system.test_status import TestStatus
from src.test.base_with_context_test import BaseWithContextTest
from src.utils.exceptions import TestNotFoundException, TestNotValidException, NotAuthorizedException, \
    TestFinishedException, TestNotFinishedException, AnswerIdNotFoundException

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

    def test_update_answer(self):
        premium_logic.add_premium(1)
        test_logic.generate_test(1)
        test = Test.find_by_lesson_id_and_account_id(1, 1)[0]
        answer = Answer.find_by_solved_test_id(test.id)[0]
        self.assertEqual(None, answer.student_answer)
        self.assertEqual(None, answer.teacher_remark)
        self.assertEqual(None, answer.points_earned)
        answer_logic.update({
            "id": answer.id,
            "student_answer": "A",
            "teacher_remark": "remark",
            "points_earned": 1.0
        })
        answer = Answer.find_by_solved_test_id(test.id)[0]
        self.assertEqual('A', answer.student_answer)
        self.assertEqual(None, answer.teacher_remark)
        self.assertEqual(None, answer.points_earned)

        student_teacher_logic.make_request(2, 1)
        self.login_as_user()
        student_teacher_logic.make_request(2, 1)
        test.end_datetime = datetime.utcnow() - timedelta(seconds=5)

        answer_logic.update({
            "id": answer.id,
            "student_answer": "A",
            "teacher_remark": "remark",
            "points_earned": 1.0
        })
        answer = Answer.find_by_solved_test_id(test.id)[0]
        self.assertEqual('A', answer.student_answer)
        self.assertEqual('remark', answer.teacher_remark)
        self.assertEqual(1.0, answer.points_earned)

    def test_get_answers(self):
        premium_logic.add_premium(1)
        test_logic.generate_test(1)
        test = Test.find_by_lesson_id_and_account_id(1, 1)[0]
        answers = answer_logic.get_answers_for_test(test.id)
        self.assertEqual(1, answers['answers'][0]['id'])
        self.assertEqual(None, answers['answers'][0]['student_answer'])
        self.assertEqual(None, answers['answers'][0]['teacher_remark'])
        self.assertEqual(None, answers['answers'][0]['points_earned'])


    def test_update_answer_exceptions(self):
        premium_logic.add_premium(1)
        test_logic.generate_test(1)
        test = Test.find_by_lesson_id_and_account_id(1, 1)[0]
        test.end_datetime = datetime.utcnow() - timedelta(seconds=5)
        test.save_to_db()

        self.assertRaises(AnswerIdNotFoundException, answer_logic.update, {
            "id": 321,
            "student_answer": "A",
            "teacher_remark": "remark",
            "points_earned": 1.0
        })
        self.assertRaises(TestFinishedException, answer_logic.update, {
            "id": 1,
            "student_answer": "A",
            "teacher_remark": "remark",
            "points_earned": 1.0
        })

        student_teacher_logic.make_request(2, 1)
        self.login_as_user()
        student_teacher_logic.make_request(2, 1)
        test.end_datetime = datetime.utcnow() + timedelta(hours=5)
        test.save_to_db()
        self.assertRaises(TestNotFinishedException, answer_logic.update, {
            "id": 1,
            "student_answer": "A",
            "teacher_remark": "remark",
            "points_earned": 1.0
        })

        account = account_logic.create_account_with_password('jill', 'jill@example.com', 'pass')
        self.login_as(account)
        self.assertRaises(NotAuthorizedException, answer_logic.update, {
            "id": 1,
            "student_answer": "A",
            "teacher_remark": "remark",
            "points_earned": 1.0
        })