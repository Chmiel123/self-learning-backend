from datetime import datetime

from src.models.content.category import Category
from src.models.system.language import Language

categories = [
    ['Maths', 'Maths is the queen of all sciences.', None, False],
    ['Geography', 'Learn all the countries and capitals.', None, True],
    ['Chemistry', 'Be careful not to blow anything up.', None, True],
    ['Biology', 'All the squishy parts.', None, True],
    ['Geometry', 'Description.', 1, True],
    ['Calculus', 'Description.', 1, True],
    ['Topology', 'Description.', 1, True]
]
lang = Language.find_by_code('en')
for cat in categories:
    category = Category()
    category.name = cat[0]
    category.content = cat[1]
    category.language_id = lang.id
    category.parent_id = cat[2]
    category.can_add_courses = cat[3]
    category.created_date = datetime(2012, 12, 12)
    category.save_to_db()
