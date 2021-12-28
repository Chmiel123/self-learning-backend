from src.logic import account_logic
from src.models.account.account import Account
from src.models.content.category import Category
from src.models.content.category_course_link import CategoryCourseLink
from src.models.content.change_history import ChangeHistory
from src.models.content.course import Course
from src.models.system.entity_status import EntityStatus
from src.models.system.entity_type import EntityType
from src.utils import modify
from src.utils.exceptions import LessonGroupIdNotFoundException, NotAuthorizedException


def get_course_by_id(course_id: int) -> object:
    course = Course.find_by_id(course_id)
    links = CategoryCourseLink.find_by_course_id(course_id)
    result = course.to_dict()
    result.update({'category_ids': [link.category_id for link in links]})
    return result


def get_courses_for_category(category_id: int, page_number: int, page_size: int) -> object:
    courses = Course.find_by_category_id(category_id, page_number, page_size)
    return {
        'courses': [x.to_dict() for x in courses]
    }


def create_or_update(course_dict: dict) -> Course:
    current_account = account_logic.get_current_account()
    if course_dict['id']:
        course = Course.find_by_id(course_dict['id'])
        if course:
            admin_privilege = account_logic.get_current_admin_privilege(current_account,
                                                                        course_dict['language_id'])
            if current_account.id == course.author_id or admin_privilege:
                course = _update(course, course_dict, current_account)
                return course.to_dict()
            else:
                raise NotAuthorizedException()
        else:
            raise LessonGroupIdNotFoundException([course_dict['id']])
    category = _create(course_dict, current_account)
    return category.to_dict()


def delete(id: int):
    course = Category.find_by_id(id)
    if course:
        current_account = account_logic.get_current_account()
        admin_privilege = account_logic.get_current_admin_privilege(current_account, course.language_id)
        if current_account.id == course.author_id or admin_privilege:
            if course.status != EntityStatus.deleted:
                if course.status == EntityStatus.active:
                    for parent_category in course.get_parents():
                        parent_category.nr_active_courses -= 1
                        parent_category.save_to_db()
                course.status = EntityStatus.deleted
                course.save_to_db()
                change_history = ChangeHistory(current_account.id, course.id, EntityType.category,
                                               course.name, course.content, course.status)
                change_history.save_to_db()
        return course.to_dict()
    else:
        raise LessonGroupIdNotFoundException([str(id)])


def _create(course_dict: dict, current_account: Account):
    course = Course()
    course.language_id = course_dict['language_id']
    course.author_id = current_account.id
    course.name = course_dict['name']
    course.content = course_dict['content']
    course.status = EntityStatus.draft
    course.save_to_db()
    for category_id in course_dict['category_ids']:
        CategoryCourseLink(category_id, course.id).save_to_db()
    change_history = ChangeHistory(current_account.id, course.id, EntityType.course, course.name,
                                   course.content, course.status)
    change_history.save_to_db()
    return course


def _update(course: Course, course_dict: dict, current_account: Account) -> Course:
    changed = False
    changed = modify(course, course_dict['name'], 'name', changed)
    changed = modify(course, course_dict['content'], 'content', changed)
    if course.status != EntityStatus.active\
            and EntityStatus(course_dict['status']) == EntityStatus.active:
        for parent_category in course.get_parents():
            parent_category.nr_active_courses += 1
            parent_category.save_to_db()
    elif course.status == EntityStatus.active\
            and EntityStatus(course_dict['status']) != EntityStatus.active:
        for parent_category in course.get_parents():
            parent_category.nr_active_courses -= 1
            parent_category.save_to_db()
    changed = modify(course, EntityStatus(course_dict['status']), 'status', changed)

    existing_links = CategoryCourseLink.find_by_course_id(course.id)
    existing_links_stay = []
    for existing_link in existing_links:
        if existing_link not in course_dict['category_ids']:
            CategoryCourseLink.delete_by_category_id_course_id(existing_link.category_id, existing_link.course_id)
        else:
            existing_links_stay.append(existing_link)

    for category_id in course_dict['category_ids']:
        create_new_link = True
        for existing_link_stay in existing_links_stay:
            if existing_link_stay.category_id == category_id:
                create_new_link = False
        if create_new_link:
            CategoryCourseLink(category_id, course.id).save_to_db()

    if changed:
        change_history = ChangeHistory(current_account.id, course.id, EntityType.course, course.name,
                                       course.content, course.status)
        change_history.save_to_db()
    return course

