from src.models.account.account import Account
from src.models.content.account_entity_tag import AccountEntityTag
from src.models.system.entity_type import EntityType
from src.models.system.language import Language

list_of_tags = [
    [1],
    [2],
    [6]
]
lang = Language.find_by_code('en')
account = Account.find_by_username('john')
for t in list_of_tags:
    tag = AccountEntityTag()
    tag.account_id = account.id
    tag.entity_id = t[0]
    tag.entity_type = EntityType.category
    tag.set_like(True)
    tag.set_favorite(True)
    tag.save_to_db()
