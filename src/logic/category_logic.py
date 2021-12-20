from src.models.system.category import Category


def get_categories() -> 'List[Category]':
    return Category.find_all()
