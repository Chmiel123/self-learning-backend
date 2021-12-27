from src.models.content.lesson_group import LessonGroup


def get_lesson_groups_for_category(category_id: int, page_number: int, page_size: int) -> object:
    lesson_groups = LessonGroup.find_by_category_id(category_id, page_number, page_size)
    return {
        'lesson_groups': [x.to_dict() for x in lesson_groups]
    }


def create_or_update(lesson_group_dict: dict):
    pass


def delete(id: int):
    pass
