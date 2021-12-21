from src.models.system.category import Category
from src.models.system.category_category_link import CategoryCategoryLink
from src.models.system.language import Language
from src.utils.error_code import ErrorCode
from src.utils.exceptions import ErrorException


def get_all_categories_for_language(language_code: str) -> object:
    language = Language.find_by_code(language_code)
    if not language:
        raise ErrorException(ErrorCode.LANGUAGE_CODE_NOT_FOUND, [language_code],
                             f'Language code {language_code} doesn\'t exist.')
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
