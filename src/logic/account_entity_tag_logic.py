from src.logic import account_logic
from src.models.account.account import Account
from src.models.content.account_entity_tag import AccountEntityTag
from src.models.system.entity_type import EntityType
from src.utils import parse_id_range, modify
from src.utils.exceptions import AccountEntityTagIdNotFoundException


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


def delete(id: int):
    tag = AccountEntityTag.find_by_id(id)
    if tag:
        AccountEntityTag.delete_by_id(id)
    else:
        raise AccountEntityTagIdNotFoundException([id])


def _create(account_entity_tag_dict: dict, current_account: Account) -> AccountEntityTag:
    tag = AccountEntityTag()
    tag.account_id = current_account.id
    tag.entity_id = account_entity_tag_dict['entity_id']
    tag.entity_type = EntityType(account_entity_tag_dict['entity_type'])
    # TODO: check if both true raise exception
    # TODO: increment like and dislike
    tag.like = account_entity_tag_dict['like']
    tag.dislike = account_entity_tag_dict['dislike']
    tag.favorite = account_entity_tag_dict['favorite']
    tag.in_progress = account_entity_tag_dict['in_progress']
    tag.completed = account_entity_tag_dict['completed']
    tag.save_to_db()
    return tag


def _update(tag: AccountEntityTag, account_entity_tag_dict: dict) -> AccountEntityTag:
    changed = False
    if tag.like and not account_entity_tag_dict['like']:
        _change_like(-1, account_entity_tag_dict['entity_id'], EntityType(account_entity_tag_dict['entity_type']))
    elif not tag.like and account_entity_tag_dict['like']:
        _change_like(+1, account_entity_tag_dict['entity_id'], EntityType(account_entity_tag_dict['entity_type']))
    changed = modify(tag, account_entity_tag_dict['like'], 'like', changed)
    if tag.dislike and not account_entity_tag_dict['dislike']:
        _change_dislike(-1, account_entity_tag_dict['entity_id'], EntityType(account_entity_tag_dict['entity_type']))
    elif not tag.dislike and account_entity_tag_dict['dislike']:
        _change_dislike(+1, account_entity_tag_dict['entity_id'], EntityType(account_entity_tag_dict['entity_type']))
    changed = modify(tag, account_entity_tag_dict['dislike'], 'dislike', changed)
    changed = modify(tag, account_entity_tag_dict['favorite'], 'favorite', changed)
    changed = modify(tag, account_entity_tag_dict['in_progress'], 'in_progress', changed)
    changed = modify(tag, account_entity_tag_dict['completed'], 'completed', changed)
    if changed:
        tag.save_to_db()
    return tag


def _change_like(change: int, entity_id: int, entity_type: EntityType):
    # TODO: change like
    pass


def _change_dislike(change: int, entity_id: int, entity_type: EntityType):
    # TODO: change dislike
    pass
