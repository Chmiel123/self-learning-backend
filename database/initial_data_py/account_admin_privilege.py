from src.models.account.account import Account
from src.models.account.admin_privilege import AdminPrivilege
from src.models.system.language import Language

found_account = Account.find_by_username("john")
lang = Language.find_by_code('en')

admin_privilege = AdminPrivilege()
admin_privilege.account_id = found_account.id
admin_privilege.language_id = lang.id
admin_privilege.strength = 5
admin_privilege.save_to_db()
