from src.logic import question_logic
from src.models.content.category import Category
from src.models.content.category_course_link import CategoryCourseLink
from src.models.content.course import Course
from src.models.content.lesson import Lesson
from src.models.content.question import Question
from src.models.system.entity_status import EntityStatus
from src.test.base_with_context_test import BaseWithContextTest
from src.utils.exceptions import QuestionIdNotFoundException, NotAuthorizedException, LessonIdNotFoundException


class QuestionLogicTest(BaseWithContextTest):
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
        CategoryCourseLink(1, 1).save_to_db()
        lesson = Lesson()
        lesson.name = 'c'
        lesson.content = 'c is a lesson'
        lesson.language_id = 1
        lesson.author_id = 1
        lesson.course_id = course1.id
        lesson.save_to_db()

    def test_create_question(self):
        question_logic.create_or_update({
            "id": None,
            "lesson_id": 1,
            "order_begin": 2,
            "order_end": 3,
            "question": "What is 2 + 2?\nA: 2\nB: 3\nC: 4\nD: 5",
            "available_answers": ['A', 'B', 'C', 'D'],
            "correct_answers": ['C'],
            "solution": "Explanation goes here."
        })
        question = Question.find_by_id(1)
        self.assertEqual(1, question.id)
        self.assertEqual(1, question.lesson_id)
        self.assertEqual(2, question.order_begin)
        self.assertEqual(3, question.order_end)
        self.assertEqual("What is 2 + 2?\nA: 2\nB: 3\nC: 4\nD: 5", question.question)
        self.assertEqual("['A', 'B', 'C', 'D']", question.available_answers)
        self.assertEqual("['C']", question.correct_answers)
        self.assertEqual("Explanation goes here.", question.solution)

    def test_create_update_question(self):
        question_logic.create_or_update({
            "id": None,
            "lesson_id": 1,
            "order_begin": 2,
            "order_end": 3,
            "question": "What is 2 + 2?\nA: 2\nB: 3\nC: 4\nD: 5",
            "available_answers": ['A', 'B', 'C', 'D'],
            "correct_answers": ['C'],
            "solution": "Explanation goes here."
        })
        question = Question.find_by_id(1)
        self.assertEqual(1, question.id)
        self.assertEqual(1, question.lesson_id)
        self.assertEqual(2, question.order_begin)
        self.assertEqual(3, question.order_end)
        self.assertEqual("What is 2 + 2?\nA: 2\nB: 3\nC: 4\nD: 5", question.question)
        self.assertEqual("['A', 'B', 'C', 'D']", question.available_answers)
        self.assertEqual("['C']", question.correct_answers)
        self.assertEqual("Explanation goes here.", question.solution)
        question_logic.create_or_update({
            "id": 1,
            "lesson_id": 1,
            "order_begin": 4,
            "order_end": 5,
            "question": "What is 2 + 3?\nA: 2\nB: 3\nC: 4\nD: 5",
            "available_answers": ['A', 'B', 'C', 'D'],
            "correct_answers": ['D'],
            "solution": "Explanation goes here."
        })
        question = Question.find_by_id(1)
        self.assertEqual(1, question.id)
        self.assertEqual(1, question.lesson_id)
        self.assertEqual(4, question.order_begin)
        self.assertEqual(5, question.order_end)
        self.assertEqual("What is 2 + 3?\nA: 2\nB: 3\nC: 4\nD: 5", question.question)
        self.assertEqual("['A', 'B', 'C', 'D']", question.available_answers)
        self.assertEqual("['D']", question.correct_answers)
        self.assertEqual("Explanation goes here.", question.solution)
        question_logic.create_or_update({
            "id": 1,
            "lesson_id": 1,
            "order_begin": 4,
            "order_end": 5,
            "question": "What is 2 + 3?\nA: 2\nB: 3\nC: 4\nD: 5",
            "available_answers": ['A', 'B', 'C', 'D'],
            "correct_answers": ['D'],
            "solution": "Explanation goes here."
        })
        question = Question.find_by_id(1)
        self.assertEqual(1, question.id)
        self.assertEqual(1, question.lesson_id)
        self.assertEqual(4, question.order_begin)
        self.assertEqual(5, question.order_end)
        self.assertEqual("What is 2 + 3?\nA: 2\nB: 3\nC: 4\nD: 5", question.question)
        self.assertEqual("['A', 'B', 'C', 'D']", question.available_answers)
        self.assertEqual("['D']", question.correct_answers)
        self.assertEqual("Explanation goes here.", question.solution)

    def test_get_questions_for_lesson(self):
        question_logic.create_or_update({
            "id": None,
            "lesson_id": 1,
            "order_begin": 2,
            "order_end": 3,
            "question": "Question 1",
            "available_answers": ['A', 'B', 'C', 'D'],
            "correct_answers": ['C'],
            "solution": "Explanation goes here."
        })
        question_logic.create_or_update({
            "id": None,
            "lesson_id": 1,
            "order_begin": 4,
            "order_end": 5,
            "question": "Question 2",
            "available_answers": ['A', 'B', 'C', 'D'],
            "correct_answers": ['C'],
            "solution": "Explanation goes here."
        })
        result = question_logic.get_questions_for_lesson(1)
        self.assertEqual(1, result['questions'][0]['id'])
        self.assertEqual("Question 1", result['questions'][0]['question'])
        self.assertEqual(2, result['questions'][1]['id'])
        self.assertEqual("Question 2", result['questions'][1]['question'])

    def test_delete(self):
        question_logic.create_or_update({
            "id": None,
            "lesson_id": 1,
            "order_begin": 2,
            "order_end": 3,
            "question": "Question 1",
            "available_answers": ['A', 'B', 'C', 'D'],
            "correct_answers": ['C'],
            "solution": "Explanation goes here."
        })
        question_logic.delete(1)
        question = Question.find_by_id(1)
        self.assertIsNone(question)
        self.assertRaises(QuestionIdNotFoundException, question_logic.delete, 1)

    def test_not_authorized_to_update(self):
        question_logic.create_or_update({
            "id": None,
            "lesson_id": 1,
            "order_begin": 2,
            "order_end": 3,
            "question": "Question 1",
            "available_answers": ['A', 'B', 'C', 'D'],
            "correct_answers": ['C'],
            "solution": "Explanation goes here."
        })
        self.login_as_user()
        self.assertRaises(NotAuthorizedException,
                          question_logic.create_or_update, {
                                "id": 1,
                                "lesson_id": 1,
                                "order_begin": 2,
                                "order_end": 3,
                                "question": "Question 1",
                                "available_answers": ['A', 'B', 'C', 'D'],
                                "correct_answers": ['C'],
                                "solution": "Explanation goes here."
                            })
        self.assertRaises(NotAuthorizedException, question_logic.delete, 1)

    def test_id_not_found(self):
        self.assertRaises(QuestionIdNotFoundException,
                          question_logic.create_or_update, {
                                "id": 1,
                                "lesson_id": 1,
                                "order_begin": 2,
                                "order_end": 3,
                                "question": "Question 1",
                                "available_answers": ['A', 'B', 'C', 'D'],
                                "correct_answers": ['C'],
                                "solution": "Explanation goes here."
                            })
        self.assertRaises(QuestionIdNotFoundException, question_logic.delete, 3)

    def test_lesson_id_not_found(self):
        self.assertRaises(LessonIdNotFoundException,
                          question_logic.create_or_update, {
                                "id": None,
                                "lesson_id": 2,
                                "order_begin": 2,
                                "order_end": 3,
                                "question": "Question 1",
                                "available_answers": ['A', 'B', 'C', 'D'],
                                "correct_answers": ['C'],
                                "solution": "Explanation goes here."
                            })