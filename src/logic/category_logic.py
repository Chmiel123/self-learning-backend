from src.models.content.category import Category
from src.models.content.category_category_link import CategoryCategoryLink
from src.models.system.language import Language
from src.utils.error_code import ErrorCode
from src.utils.exceptions import ErrorException


def get_all_categories_for_language(language_code: str) -> object:
    language = Language.find_by_code(language_code)
    categories = Category.find_by_language_id(language.id)
    category_links = CategoryCategoryLink.find_by_language_id(language.id)
    return {
        'categories': [x.serialize() for x in categories],
        'category_links': [x.serialize() for x in category_links]
    }


def create_or_update(category_dict: dict) -> Category:
    if category_dict['id']:
        category = Category.find_by_id(category_dict['id'])
        if category:
            category.content = category_dict['content']
            category.save_to_db()
            return category.serialize()
        else:
            raise ErrorException(ErrorCode.CATEGORY_ID_NOT_FOUND, [category_dict['id']],
                                 f'Category id: {category_dict["id"]} not found.')
    category = Category(category_dict['name'], category_dict['content'], category_dict['language_id'])
    category.save_to_db()
    return category.serialize()
