from src.models import EntityType, Comment
from src.models.account.account import Account
from src.models.system.language import Language

comments = [
    ['This is a comment 1', 1, EntityType.course, 1, 2],
    ['This is a comment 2', 1, EntityType.course, 1, 0],
    ['This is a comment 3', 1, EntityType.course, 1, 0],
    ['This is a comment 4', 1, EntityType.course, 1, 0],
    ['This is a comment 1 1', 1, EntityType.comment, 2, 0],
    ['This is a comment 1 2', 1, EntityType.comment, 2, 0],
]

lang = Language.find_by_code('en')
account = Account.find_by_username('john')

for c in comments:
    comment = Comment()
    comment.language_id = lang.id
    comment.author_id = account.id
    comment.content = c[0]
    comment.parent_id = c[1]
    comment.parent_type = c[2]
    comment.depth = c[3]
    comment.replies = c[4]
    comment.save_to_db()
