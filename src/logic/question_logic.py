from typing import Dict, List

from src.logic import account_logic, lesson_logic
from src.models.content.lesson import Lesson
from src.models.content.question import Question
from src.utils import modify
from src.utils.exceptions import QuestionIdNotFoundException, NotAuthorizedException, LessonIdNotFoundException


def get_questions_for_lesson(lesson_id: int) -> Dict[str, List[Dict[str, str]]]:
    questions = Question.find_by_lesson_id(lesson_id)
    return {
        'questions': [x.to_dict() for x in questions]
    }


def create_or_update(question_dict: dict) -> Question:
    current_account = account_logic.get_current_account()
    lesson = Lesson.find_by_id(question_dict['lesson_id'])
    if not lesson:
        raise LessonIdNotFoundException([question_dict['lesson_id']])
    admin_privilege = account_logic.get_current_admin_privilege(current_account, lesson.language_id)
    if current_account.id == lesson.author_id or admin_privilege:
        if question_dict['id']:
            question = Question.find_by_id(question_dict['id'])
            if question:
                question = _update(question, question_dict)
                lesson_logic.validate_test(lesson)
                return question.to_dict()
            else:
                raise QuestionIdNotFoundException([question_dict['id']])
        question = _create(question_dict)
        lesson_logic.validate_test(lesson)
        return question.to_dict()
    else:
        raise NotAuthorizedException()


def delete(id: int):
    question = Question.find_by_id(id)
    if question:
        lesson = Lesson.find_by_id(question.lesson_id)
        current_account = account_logic.get_current_account()
        admin_privilege = account_logic.get_current_admin_privilege(current_account, lesson.language_id)
        if current_account.id == lesson.author_id or admin_privilege:
            Question.delete_by_id(id)
        else:
            raise NotAuthorizedException()
    else:
        raise QuestionIdNotFoundException(id)


def _create(question_dict: dict):
    question = Question()
    question.lesson_id = question_dict['lesson_id']
    question.order_begin = question_dict['order_begin']
    question.order_end = question_dict['order_end']
    question.question = question_dict['question']
    question.available_answers = str(question_dict['available_answers'])
    question.correct_answers = str(question_dict['correct_answers'])
    question.solution = question_dict['solution']
    question.lesson_id = question_dict['lesson_id']
    question.save_to_db()
    return question


def _update(question: Question, question_dict: dict) -> Question:
    changed = False
    changed = modify(question, question_dict['order_begin'], 'order_begin', changed)
    changed = modify(question, question_dict['order_end'], 'order_end', changed)
    changed = modify(question, question_dict['question'], 'question', changed)
    changed = modify(question, str(question_dict['available_answers']), 'available_answers', changed)
    changed = modify(question, str(question_dict['correct_answers']), 'correct_answers', changed)
    changed = modify(question, question_dict['solution'], 'solution', changed)
    changed = modify(question, question_dict['lesson_id'], 'lesson_id', changed)
    if changed:
        question.save_to_db()
    return question
