import random
from typing import List

from src.logic import account_logic, premium_logic
from src.models import Lesson
from src.models.account.account import Account
from src.models.content.answer import Answer
from src.models.content.question import Question, rules_to_student
from src.models.content.test import Test
from src.models.system.lesson_type import LessonType
from src.models.system.test_status import TestStatus
from src.utils.exceptions import TestNotFoundException


def generate_test(lesson_id: int):
    lesson = Lesson.find_by_id(lesson_id)
    if not lesson or lesson.type != LessonType.test:
        raise TestNotFoundException([str(lesson_id)])
    questions = Question.find_by_lesson_id(lesson_id)
    questions.sort(key=lambda question: question.order_begin)
    selected_questions: List[Question] = []
    current_order_begin = 1
    current_order_end = 1
    question_pool = []
    for question in questions:
        if question.order_begin <= current_order_begin <= question.order_end:
            question_pool.append(question)
            current_order_end = question.order_end
        else:
            selected_questions += random.sample(question_pool, current_order_end - current_order_begin + 1)
            current_order_begin = current_order_end + 1
            current_order_end += 1
            question_pool = [question]
    selected_questions += random.sample(question_pool, current_order_end - current_order_begin + 1)

    current_account = account_logic.get_current_account()
    is_premium = premium_logic.is_premium(current_account.id)
    if is_premium:
        save_test(current_account, lesson, selected_questions)
    return {
        'questions': [x.to_dict(rules=rules_to_student) for x in selected_questions]
    }


def save_test(account: Account, lesson: Lesson, selected_questions: List[Question]):
    test = Test()
    test.test_id = lesson.id
    test.solver_id = account.id
    test.save_to_db()
    for i in range(len(selected_questions)):
        answer = Answer()
        answer.test_id = test.id
        answer.question_id = selected_questions[i].id
        answer.order = i + 1
        answer.save_to_db()
