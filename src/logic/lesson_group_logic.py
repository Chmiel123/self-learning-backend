from src.logic import account_logic
from src.models.account.account import Account
from src.models.content.category import Category
from src.models.content.category_group_link import CategoryGroupLink
from src.models.content.change_history import ChangeHistory
from src.models.content.lesson_group import LessonGroup
from src.models.system.entity_status import EntityStatus
from src.models.system.entity_type import EntityType
from src.utils import modify
from src.utils.exceptions import LessonGroupIdNotFoundException, NotAuthorizedException


def get_lesson_group_by_id(lesson_group_id: int) -> object:
    lesson_group = LessonGroup.find_by_id(lesson_group_id)
    links = CategoryGroupLink.find_by_group_id(lesson_group_id)
    result = lesson_group.to_dict()
    result.update({'category_ids': [link.category_id for link in links]})
    return result


def get_lesson_groups_for_category(category_id: int, page_number: int, page_size: int) -> object:
    lesson_groups = LessonGroup.find_by_category_id(category_id, page_number, page_size)
    return {
        'lesson_groups': [x.to_dict() for x in lesson_groups]
    }


def create_or_update(lesson_group_dict: dict) -> LessonGroup:
    current_account = account_logic.get_current_account()
    if lesson_group_dict['id']:
        lesson_group = LessonGroup.find_by_id(lesson_group_dict['id'])
        if lesson_group:
            admin_privilege = account_logic.get_current_admin_privilege(current_account,
                                                                        lesson_group_dict['language_id'])
            if current_account.id == lesson_group.author_id or admin_privilege:
                lesson_group = _update(lesson_group, lesson_group_dict, current_account)
                return lesson_group.to_dict()
            else:
                raise NotAuthorizedException()
        else:
            raise LessonGroupIdNotFoundException([lesson_group_dict['id']])
    category = _create(lesson_group_dict, current_account)
    return category.to_dict()


def delete(id: int):
    lesson_group = Category.find_by_id(id)
    if lesson_group:
        current_account = account_logic.get_current_account()
        admin_privilege = account_logic.get_current_admin_privilege(current_account, lesson_group.language_id)
        if current_account.id == lesson_group.author_id or admin_privilege:
            if lesson_group.status != EntityStatus.deleted:
                if lesson_group.status == EntityStatus.active:
                    for parent_category in lesson_group.get_parents():
                        parent_category.nr_active_lesson_groups -= 1
                        parent_category.save_to_db()
                lesson_group.status = EntityStatus.deleted
                lesson_group.save_to_db()
                change_history = ChangeHistory(current_account.id, lesson_group.id, EntityType.category,
                                               lesson_group.name, lesson_group.content, lesson_group.status)
                change_history.save_to_db()
        return lesson_group.to_dict()
    else:
        raise LessonGroupIdNotFoundException([str(id)])


def _create(lesson_group_dict: dict, current_account: Account):
    lesson_group = LessonGroup()
    lesson_group.language_id = lesson_group_dict['language_id']
    lesson_group.author_id = current_account.id
    lesson_group.name = lesson_group_dict['name']
    lesson_group.content = lesson_group_dict['content']
    lesson_group.status = EntityStatus.draft
    lesson_group.save_to_db()
    for category_id in lesson_group_dict['category_ids']:
        CategoryGroupLink(category_id, lesson_group.id).save_to_db()
    change_history = ChangeHistory(current_account.id, lesson_group.id, EntityType.lesson_group, lesson_group.name,
                                   lesson_group.content, lesson_group.status)
    change_history.save_to_db()
    return lesson_group


def _update(lesson_group: LessonGroup, lesson_group_dict: dict, current_account: Account) -> LessonGroup:
    changed = False
    changed = modify(lesson_group, lesson_group_dict['name'], 'name', changed)
    changed = modify(lesson_group, lesson_group_dict['content'], 'content', changed)
    if lesson_group.status != EntityStatus.active\
            and EntityStatus(lesson_group_dict['status']) == EntityStatus.active:
        for parent_category in lesson_group.get_parents():
            parent_category.nr_active_lesson_groups += 1
            parent_category.save_to_db()
    elif lesson_group.status == EntityStatus.active\
            and EntityStatus(lesson_group_dict['status']) != EntityStatus.active:
        for parent_category in lesson_group.get_parents():
            parent_category.nr_active_lesson_groups -= 1
            parent_category.save_to_db()
    changed = modify(lesson_group, EntityStatus(lesson_group_dict['status']), 'status', changed)

    existing_links = CategoryGroupLink.find_by_group_id(lesson_group.id)
    existing_links_stay = []
    for existing_link in existing_links:
        if existing_link not in lesson_group_dict['category_ids']:
            CategoryGroupLink.delete_by_category_id_group_id(existing_link.category_id, existing_link.group_id)
        else:
            existing_links_stay.append(existing_link)

    for category_id in lesson_group_dict['category_ids']:
        create_new_link = True
        for existing_link_stay in existing_links_stay:
            if existing_link_stay.category_id == category_id:
                create_new_link = False
        if create_new_link:
            CategoryGroupLink(category_id, lesson_group.id).save_to_db()

    if changed:
        change_history = ChangeHistory(current_account.id, lesson_group.id, EntityType.lesson_group, lesson_group.name,
                                       lesson_group.content, lesson_group.status)
        change_history.save_to_db()
    return lesson_group

