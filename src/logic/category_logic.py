from src.models.content.category import Category
from src.models.content.category_category_link import CategoryCategoryLink
from src.models.system.language import Language


def get_all_categories_for_language(language_code: str) -> object:
    language = Language.find_by_code(language_code)
    categories = Category.find_by_language_id(language.id)
    categories_serialized = []
    for category in categories:
        category_serialized = category.serialize()
        category_serialized.update({'language': language_code})
        categories_serialized.append(category_serialized)
    category_links = CategoryCategoryLink.find_by_language_id(language.id)
    return {
        'categories': categories_serialized,
        'category_links': [x.serialize() for x in category_links]
    }


def create_or_update(category_dict: dict):
    if category_dict['id']:
        category = Category.find_by_id(category_dict['id'])
        if category:
            category.content = category_dict['content']
            category.save_to_db()
            return
    language = Language.find_by_code(category_dict['language'])
    category = Category(category_dict['name'], category_dict['content'], language.id)
    category.save_to_db()
    return
