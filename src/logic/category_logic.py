from typing import Dict, List

from src.logic import account_logic
from src.models.account.account import Account
from src.models.content.category import Category
from src.models.content.change_history import ChangeHistory
from src.models.system.entity_status import EntityStatus
from src.models.system.entity_type import EntityType
from src.models.system.language import Language
from src.utils import modify
from src.utils.exceptions import CategoryIdNotFoundException


def get_all_categories_for_language(language_code: str) -> Dict[str, List[Dict[str, str]]]:
    language = Language.find_by_code(language_code)
    categories = Category.find_by_language_id(language.id)
    return {
        'categories': [x.to_dict() for x in categories]
    }


def create_or_update(category_dict: dict) -> Category:
    current_account = account_logic.check_if_admin_privilege(category_dict['language_id'])
    if category_dict['id']:
        category = Category.find_by_id(category_dict['id'])
        if category:
            category = _update(category, category_dict, current_account)
            return category.to_dict()
        else:
            raise CategoryIdNotFoundException([category_dict['id']])
    category = _create(category_dict, current_account)
    return category.to_dict()


def delete(id: int):
    category = Category.find_by_id(id)
    if category:
        account_logic.check_if_admin_privilege(category.language_id)
        if category.status != EntityStatus.deleted:
            category.status = EntityStatus.deleted
            category.save_to_db()
            current_account = account_logic.get_current_account()
            change_history = ChangeHistory(current_account.id, category.id, EntityType.category, category.name,
                                           category.content, category.status)
            change_history.save_to_db()
        return category.to_dict()
    else:
        raise CategoryIdNotFoundException([str(id)])


def _create(category_dict: dict, current_account: Account):
    category = Category()
    category.language_id = category_dict['language_id']
    category.author_id = current_account.id
    category.parent_id = category_dict['parent_id']
    category.name = category_dict['name']
    category.content = category_dict['content']
    category.can_add_courses = category_dict['can_add_courses']
    category.status = EntityStatus.draft
    category.save_to_db()
    change_history = ChangeHistory(current_account.id, category.id, EntityType.category, category.name,
                                   category.content, category.status)
    change_history.save_to_db()
    return category


def _update(category: Category, category_dict: dict, current_account: Account) -> Category:
    changed = False
    changed = modify(category, category_dict['parent_id'], 'parent_id', changed)
    changed = modify(category, category_dict['name'], 'name', changed)
    changed = modify(category, category_dict['content'], 'content', changed)
    changed = modify(category, category_dict['can_add_courses'], 'can_add_courses', changed)
    changed = modify(category, EntityStatus(category_dict['status']), 'status', changed)
    if changed:
        change_history = ChangeHistory(current_account.id, category.id, EntityType.category, category.name,
                                       category.content, category.status)
        change_history.save_to_db()
    return category

