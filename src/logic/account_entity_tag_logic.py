from src.logic import account_logic
from src.models import get_parent_entity
from src.models.account.account import Account
from src.models.content.account_entity_tag import AccountEntityTag
from src.models.content.comment import Comment
from src.models.content.course import Course
from src.models.content.lesson import Lesson
from src.models.system.entity_type import EntityType
from src.utils import parse_id_range, modify
from src.utils.exceptions import AccountEntityTagIdNotFoundException, AccountEntityTagLikeDislikeBothTrueException, \
    AccountEntityTagInProgressCompletedBothTrueException, CourseIdNotFoundException, LessonIdNotFoundException, \
    CommentIdNotFoundException, EntityTypeNotSupportedException


def get_account_entity_tags_for_entities(entity_id_range: str, entity_type_raw: int):
    current_account = account_logic.get_current_account()
    range_start, range_end = parse_id_range(entity_id_range)
    entity_type = EntityType(entity_type_raw)
    result = AccountEntityTag.find_by_account_id_and_entity_type(current_account.id, entity_type, range_start,
                                                                 range_end)
    return {
        'account_entity_tags': [x.to_dict() for x in result]
    }


def create_or_update(account_entity_tag_dict: dict) -> AccountEntityTag:
    current_account = account_logic.get_current_account()
    found = AccountEntityTag.find_by_account_id_and_entity_id(current_account.id, account_entity_tag_dict['entity_id'],
                                                              EntityType(account_entity_tag_dict['entity_type']))
    if found:
        tag = _update(found, account_entity_tag_dict)
    else:
        tag = _create(account_entity_tag_dict, current_account)
    return tag.to_dict()


def delete(delete_dict: dict):
    account = account_logic.get_current_account()
    tag = AccountEntityTag.find_by_account_id_and_entity_id(account.id, delete_dict['entity_id'],
                                                            EntityType(delete_dict['entity_type']))
    if tag:
        AccountEntityTag.delete_by_account_id_and_entity_id(account.id, delete_dict['entity_id'],
                                                            EntityType(delete_dict['entity_type']))
    else:
        raise AccountEntityTagIdNotFoundException([delete_dict['entity_id'],
                                                  EntityType(delete_dict['entity_type'])])


def _create(account_entity_tag_dict: dict, current_account: Account) -> AccountEntityTag:
    tag = AccountEntityTag()
    tag.account_id = current_account.id
    tag.entity_id = account_entity_tag_dict['entity_id']
    tag.entity_type = EntityType(account_entity_tag_dict['entity_type'])
    parent_entity = get_parent_entity(tag.entity_id, tag.entity_type)

    if account_entity_tag_dict['like'] == 'true' and account_entity_tag_dict['dislike'] == 'true':
        raise AccountEntityTagLikeDislikeBothTrueException()
    tag.like = account_entity_tag_dict['like'] == 'true'
    if tag.like:
        _change_like(+1, parent_entity)
    tag.dislike = account_entity_tag_dict['dislike'] == 'true'
    if tag.dislike:
        _change_dislike(+1, parent_entity)
    tag.favorite = account_entity_tag_dict['favorite'] == 'true'
    if account_entity_tag_dict['in_progress'] == 'true' and account_entity_tag_dict['completed'] == 'true':
        raise AccountEntityTagInProgressCompletedBothTrueException()
    tag.in_progress = account_entity_tag_dict['in_progress'] == 'true'
    tag.completed = account_entity_tag_dict['completed'] == 'true'
    tag.save_to_db()
    return tag


def _update(tag: AccountEntityTag, account_entity_tag_dict: dict) -> AccountEntityTag:
    parent_entity = get_parent_entity(tag.entity_id, tag.entity_type)
    changed = False
    if tag.like and not account_entity_tag_dict['like'] == 'true':
        _change_like(-1, parent_entity)
    elif not tag.like and account_entity_tag_dict['like'] == 'true':
        _change_like(+1, parent_entity)
    changed = modify(tag, account_entity_tag_dict['like'] == 'true', 'like', changed)
    if tag.dislike and not account_entity_tag_dict['dislike'] == 'true':
        _change_dislike(-1, parent_entity)
    elif not tag.dislike and account_entity_tag_dict['dislike'] == 'true':
        _change_dislike(+1, parent_entity)
    changed = modify(tag, account_entity_tag_dict['dislike'] == 'true', 'dislike', changed)
    changed = modify(tag, account_entity_tag_dict['favorite'] == 'true', 'favorite', changed)
    changed = modify(tag, account_entity_tag_dict['in_progress'] == 'true', 'in_progress', changed)
    changed = modify(tag, account_entity_tag_dict['completed'] == 'true', 'completed', changed)
    if changed:
        tag.save_to_db()
    return tag


def _change_like(change: int, parent_entity: object):
    _change(change, parent_entity, 'likes')


def _change_dislike(change: int, parent_entity: object):
    _change(change, parent_entity, 'dislikes')


def _change(change: int, parent_entity: object, field: str):
    parent_entity.__setattr__(field, parent_entity.__getattribute__(field) + change)
    parent_entity.save_to_db()
