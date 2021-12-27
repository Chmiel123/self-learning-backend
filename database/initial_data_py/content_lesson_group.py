from src.models.account.account import Account
from src.models.content.category import Category
from src.models.content.category_group_link import CategoryGroupLink
from src.models.content.lesson_group import LessonGroup
from src.models.system.entity_status import EntityStatus
from src.models.system.language import Language

list_of_lesson_groups = [
    ['Geometry 101', 'This is a great course', 5, EntityStatus.active, 150, 11, ],
    ['Geometry 102', 'This is a great course', 5, EntityStatus.active, 78, 21, ],
    ['Calculus 101', 'This is a great course', 6, EntityStatus.draft, 78, 21, ]
]
lang = Language.find_by_code('en')
account = Account.find_by_username('john')
for lg in list_of_lesson_groups:
    lesson_group = LessonGroup()
    lesson_group.author_id = account.id
    lesson_group.name = lg[0]
    lesson_group.content = lg[1]
    lesson_group.language_id = lang.id
    lesson_group.status = lg[3]
    lesson_group.likes = lg[4]
    lesson_group.dislikes = lg[5]
    lesson_group.save_to_db()
    category_group_link = CategoryGroupLink(lg[2], lesson_group.id)
    category_group_link.save_to_db()
    if lesson_group.status == EntityStatus.active:
        category = Category.find_by_id(category_group_link.category_id)
        category.nr_active_lesson_groups += 1
        category.save_to_db()
