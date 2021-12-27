from src.models.account.account import Account
from src.models.account.admin_privilege import AdminPrivilege
from src.models.system.language import Language

found_account = Account.find_by_username("john")
lang = Language.find_by_code('en')

admin_privilege = AdminPrivilege(found_account.id, 5, lang.id)