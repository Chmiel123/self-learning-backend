from typing import Dict, List

from src.logic import account_logic
from src.models.account.account import Account
from src.models.account.admin_privilege import AdminPrivilege
from src.models.content.change_history import ChangeHistory
from src.models.content.course import Course
from src.models.content.lesson import Lesson
from src.models.content.question import Question
from src.models.system.entity_status import EntityStatus
from src.models.system.entity_type import EntityType
from src.models.system.lesson_type import LessonType
from src.utils import modify
from src.utils.exceptions import LessonIdNotFoundException, NotAuthorizedException, LessonLanguageIdInvalidException, \
    CourseIdNotFoundException


def get_lesson_by_id(lesson_id: int) -> Dict[str, object]:
    lesson = Lesson.find_by_id(lesson_id)
    result = lesson.to_dict()
    return result


def get_lessons_for_course(course_id: int) -> Dict[str, List[Dict[str, str]]]:
    lessons = Lesson.find_by_course_id(course_id)
    return {
        'lessons': [x.to_dict() for x in lessons]
    }


def create_or_update(lesson_dict: dict) -> Lesson:
    current_account = account_logic.get_current_account()
    if lesson_dict['id']:
        lesson = Lesson.find_by_id(lesson_dict['id'])
        if lesson:
            admin_privilege = account_logic.get_current_admin_privilege(current_account,
                                                                        lesson_dict['language_id'])
            if current_account.id == lesson.author_id or admin_privilege:
                lesson = _update(lesson, lesson_dict, current_account)
                return lesson.to_dict()
            else:
                raise NotAuthorizedException()
        else:
            raise LessonIdNotFoundException([lesson_dict['id']])
    parent_course = Course.find_by_id(lesson_dict['course_id'])
    if parent_course:
        if lesson_dict['language_id'] != parent_course.language_id:
            raise LessonLanguageIdInvalidException([lesson_dict['language_id']])
        admin_privilege = AdminPrivilege.find_by_account_id_and_language_id(current_account.id,
                                                                            lesson_dict['language_id'])
        if parent_course.author_id != current_account.id and not admin_privilege:
            raise NotAuthorizedException()
    else:
        raise CourseIdNotFoundException([lesson_dict['course_id']])
    lesson = _create(lesson_dict, current_account)
    return lesson.to_dict()


def delete(id: int):
    lesson = Lesson.find_by_id(id)
    if lesson:
        current_account = account_logic.get_current_account()
        admin_privilege = account_logic.get_current_admin_privilege(current_account, lesson.language_id)
        if current_account.id == lesson.author_id or admin_privilege:
            if lesson.status != EntityStatus.deleted:
                lesson.status = EntityStatus.deleted
                lesson.save_to_db()
                change_history = ChangeHistory(current_account.id, lesson.id, EntityType.lesson, lesson.name,
                                               lesson.content, lesson.status)
                change_history.save_to_db()
        else:
            raise NotAuthorizedException()
        return lesson.to_dict()
    else:
        raise LessonIdNotFoundException([str(id)])


def validate_test(lesson: Lesson) -> bool:
    questions = Question.find_by_lesson_id(lesson.id)
    questions.sort(key=lambda q: q.order_begin)
    order_begin = 0
    order_end = 0
    for question in questions:
        if question.order_begin >= order_end and question.order_end >= order_end:
            order_begin = question.order_begin
            order_end = question.order_end
        elif question.order_end != order_end or question.order_begin != order_begin:
            return False
    return True


def _create(lesson_dict: dict, current_account: Account):
    lesson = Lesson()
    lesson.course_id = lesson_dict['course_id']
    lesson.language_id = lesson_dict['language_id']
    lesson.author_id = current_account.id
    lesson.name = lesson_dict['name']
    lesson.content = lesson_dict['content']
    lesson.type = LessonType(lesson_dict['type'])
    lesson.order = int(lesson_dict['order'])
    lesson.status = EntityStatus.draft
    lesson.save_to_db()
    change_history = ChangeHistory(current_account.id, lesson.id, EntityType.lesson, lesson.name,
                                   lesson.content, lesson.status)
    change_history.save_to_db()
    return lesson


def _update(lesson: Lesson, lesson_dict: dict, current_account: Account) -> Lesson:
    changed = False
    changed = modify(lesson, lesson_dict['name'], 'name', changed)
    changed = modify(lesson, lesson_dict['content'], 'content', changed)
    changed = modify(lesson, EntityStatus(lesson_dict['status']), 'status', changed)
    changed = modify(lesson, LessonType(lesson_dict['type']), 'type', changed)
    changed = modify(lesson, int(lesson_dict['order']), 'order', changed)
    if changed:
        if not validate_test(lesson):
            lesson.is_valid_test = False
        lesson.save_to_db()
        change_history = ChangeHistory(current_account.id, lesson.id, EntityType.lesson, lesson.name,
                                       lesson.content, lesson.status)
        change_history.save_to_db()
    return lesson
