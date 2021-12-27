from flask_jwt_extended import get_jwt_identity

from src.models.account.account import Account
from src.models.account.admin_privilege import AdminPrivilege
from src.models.content.category import Category
from src.models.content.category_category_link import CategoryCategoryLink
from src.models.content.change_history import ChangeHistory
from src.models.system.entity_status import EntityStatus
from src.models.system.entity_type import EntityType
from src.models.system.language import Language
from src.utils import modify
from src.utils.error_code import ErrorCode
from src.utils.exceptions import ErrorException, CategoryIdNotFoundException, AdminPrivilegeRequiredException


def get_all_categories_for_language(language_code: str) -> object:
    language = Language.find_by_code(language_code)
    categories = Category.find_by_language_id(language.id)
    category_links = CategoryCategoryLink.find_by_language_id(language.id)
    return {
        'categories': [x.serialize() for x in categories],
        'category_links': [x.serialize() for x in category_links]
    }


def create_or_update(category_dict: dict) -> Category:
    current_user = get_jwt_identity()
    current_account = Account.find_by_username(current_user)
    admin_privilege = AdminPrivilege.find_by_account_id_and_language_id(current_account.id,
                                                                        category_dict['language_id'])
    if not admin_privilege:
        raise AdminPrivilegeRequiredException()
    if category_dict['id']:
        category = Category.find_by_id(category_dict['id'])
        if category:
            category = _update(category, category_dict, current_account)
            return category.serialize()
        else:
            raise CategoryIdNotFoundException([category_dict['id']])
    category = _create(category_dict, current_account)
    return category.serialize()


def delete(id: int):
    category = Category.find_by_id(id)
    if category:
        current_user = get_jwt_identity()
        current_account = Account.find_by_username(current_user)
        admin_privilege = AdminPrivilege.find_by_account_id_and_language_id(current_account.id, category.language_id)
        if not admin_privilege:
            raise AdminPrivilegeRequiredException()
        category.status = EntityStatus.deleted
        category.save_to_db()
        return category.serialize()
    else:
        raise CategoryIdNotFoundException([str(id)])


def _create(category_dict: dict, current_account: Account):
    category = Category()
    category.language_id = category_dict['language_id']
    category.author_id = current_account.id
    category.parent_id = category_dict['parent_id']
    category.name = category_dict['name']
    category.content = category_dict['content']
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
    changed = modify(category, EntityStatus(category_dict['status']), 'status', changed)
    if changed:
        change_history = ChangeHistory(current_account.id, category.id, EntityType.category, category.name,
                                       category.content, category.status)
        change_history.save_to_db()
    return category

