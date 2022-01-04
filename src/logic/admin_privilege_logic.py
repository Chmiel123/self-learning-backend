from src.logic import account_logic
from src.models.account.admin_privilege import AdminPrivilege
from src.models.content.account_entity_tag import AccountEntityTag
from src.services import services
from src.utils import modify
from src.utils.exceptions import NotAuthorizedException, \
    AdminPrivilegeStrengthInvalidException, AdminPrivilegeNotFoundException


def get_admin_privileges_for_account(account_id: int):
    result = AdminPrivilege.find_by_account_id(account_id)
    return {
        'admin_privileges': [x.to_dict() for x in result]
    }


def create_or_update(admin_privilege_dict: dict) -> AdminPrivilege:
    current_account = account_logic.get_current_account()
    current_admin_privilege = AdminPrivilege.find_by_account_id_and_language_id(current_account.id,
                                                                                admin_privilege_dict['language_id'])
    if not current_admin_privilege:
        raise NotAuthorizedException()
    found = AdminPrivilege.find_by_account_id_and_language_id(admin_privilege_dict['account_id'],
                                                              admin_privilege_dict['language_id'])
    input_strength = int(admin_privilege_dict['strength'])
    if input_strength < services.flask.config['ADMIN_STRENGTH_MIN'] or\
       input_strength > services.flask.config['ADMIN_STRENGTH_MAX']:
        raise AdminPrivilegeStrengthInvalidException([services.flask.config['ADMIN_STRENGTH_MIN'],
                                                      services.flask.config['ADMIN_STRENGTH_MAX']])
    if input_strength >= current_admin_privilege.strength:
        raise NotAuthorizedException()
    if found:
        if found.strength >= current_admin_privilege.strength:
            raise NotAuthorizedException()
        admin_privilege = _update(found, input_strength)
    else:
        admin_privilege = _create(admin_privilege_dict['account_id'], admin_privilege_dict['language_id'],
                                  input_strength)
    return admin_privilege.to_dict()


def delete(delete_dict: dict):
    current_account = account_logic.get_current_account()
    current_admin_privilege = AdminPrivilege.find_by_account_id_and_language_id(current_account.id,
                                                                                delete_dict['language_id'])
    found = AdminPrivilege.find_by_account_id_and_language_id(delete_dict['account_id'], delete_dict['language_id'])
    if found:
        if found.strength >= current_admin_privilege.strength:
            raise NotAuthorizedException()
        AdminPrivilege.delete_by_account_id_and_language_id(delete_dict['account_id'], delete_dict['language_id'])
    else:
        raise AdminPrivilegeNotFoundException([delete_dict['account_id'], delete_dict['language_id']])


def _create(account_id: int, language_id: int, strength: int) -> AdminPrivilege:
    admin_privilege = AdminPrivilege()
    admin_privilege.account_id = account_id
    admin_privilege.language_id = language_id
    admin_privilege.strength = strength
    admin_privilege.save_to_db()
    return admin_privilege


def _update(admin_privilege: AdminPrivilege, strength: int) -> AccountEntityTag:
    changed = False
    changed = modify(admin_privilege, strength, 'strength', changed)
    if changed:
        admin_privilege.save_to_db()
    return admin_privilege
