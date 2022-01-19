import random
from datetime import datetime, timedelta
from typing import List

from flask_jwt_extended import get_jwt_identity

from src.logic import account_logic, premium_logic
from src.models import Lesson
from src.models.account.account import Account
from src.models.content.answer import Answer
from src.models.content.question import Question, rules_to_student
from src.models.content.test import Test
from src.models.system.lesson_type import LessonType
from src.utils.exceptions import TestNotFoundException, TestNotValidException


def get_tests(lesson_id: int):
    account = account_logic.get_current_account()
    tests = Test.find_by_lesson_id_and_account_id(lesson_id, account.id)
    return {
        'tests': [x.to_dict() for x in tests]
    }


def generate_test(lesson_id: int):
    lesson = Lesson.find_by_id(lesson_id)
    if not lesson or lesson.type != LessonType.test:
        raise TestNotFoundException([str(lesson_id)])
    if not lesson.is_valid_test:
        raise TestNotValidException([str(lesson_id)])
    questions = Question.find_by_lesson_id(lesson_id)
    questions.sort(key=lambda q: q.order_begin)
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

    current_account = account_logic.try_get_current_account()
    if current_account:
        is_premium = premium_logic.is_premium(current_account.id)
        if is_premium:
            _save_test(current_account, lesson, selected_questions)
    return {
        'questions': [x.to_dict(rules=rules_to_student) for x in selected_questions]
    }


def _save_test(account: Account, lesson: Lesson, selected_questions: List[Question]):
    test = Test()
    test.lesson_id = lesson.id
    test.account_id = account.id
    test.start_datetime = datetime.utcnow()
    test.start_datetime = test.start_datetime + timedelta(minutes=lesson.duration_minutes)
    test.save_to_db()
    for i in range(len(selected_questions)):
        answer = Answer()
        answer.test_id = test.id
        answer.question_id = selected_questions[i].id
        answer.order = i + 1
        answer.save_to_db()
