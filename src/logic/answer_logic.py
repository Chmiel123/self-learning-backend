from datetime import datetime
from typing import Dict, List

from src.logic import account_logic, student_teacher_logic
from src.models.content.answer import Answer
from src.models.content.test import Test
from src.utils.exceptions import AnswerIdNotFoundException, TestNotFoundException, TestFinishedException, \
    TestNotFinishedException, NotAuthorizedException


def get_answers_for_test(test_id: int) -> Dict[str, List[Dict[str, str]]]:
    answers = Answer.find_by_solved_test_id(test_id)
    return {
        'answers': [x.to_dict() for x in answers]
    }


def update(answer_dict: dict) -> Answer:
    current_account = account_logic.get_current_account()
    answer = Answer.find_by_id(answer_dict['id'])
    if not answer:
        raise AnswerIdNotFoundException([answer_dict['id']])
    test = Test.find_by_id(answer.test_id)
    if test.account_id == current_account.id:
        if datetime.utcnow() < test.end_datetime:
            answer.student_answer = answer_dict['student_answer']
            answer.save_to_db()
        else:
            raise TestFinishedException([str(test.end_datetime)])
    elif student_teacher_logic.are_linked(current_account.id, test.account_id):
        if datetime.utcnow() > test.end_datetime:
            answer.teacher_remark = answer_dict['teacher_remark']
            answer.points_earned = float(answer_dict['points_earned'])
            answer.save_to_db()
        else:
            raise TestNotFinishedException([str(test.end_datetime)])
    else:
        raise NotAuthorizedException()