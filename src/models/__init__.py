from src.models.content.category import Category
from src.models.content.comment import Comment
from src.models.content.course import Course
from src.models.content.lesson import Lesson
from src.models.system.entity_type import EntityType
from src.utils.exceptions import CourseIdNotFoundException, LessonIdNotFoundException, CommentIdNotFoundException, \
    EntityTypeNotSupportedException, CategoryIdNotFoundException


def get_tag_parent_entity(entity_id: int, entity_type: EntityType) -> object:
    parent_entity = None
    if entity_type == EntityType.category:
        parent_entity = Category.find_by_id(entity_id)
        if not parent_entity:
            raise CategoryIdNotFoundException([str(entity_id)])
    elif entity_type == EntityType.course:
        parent_entity = Course.find_by_id(entity_id)
        if not parent_entity:
            raise CourseIdNotFoundException([str(entity_id)])
    elif entity_type == EntityType.lesson:
        parent_entity = Lesson.find_by_id(entity_id)
        if not parent_entity:
            raise LessonIdNotFoundException([str(entity_id)])
    elif entity_type == EntityType.comment:
        parent_entity = Comment.find_by_id(entity_id)
        if not parent_entity:
            raise CommentIdNotFoundException([str(entity_id)])
    else:
        raise EntityTypeNotSupportedException([entity_type.value])
    return parent_entity


def get_comment_parent_entity(entity_id: int, entity_type: EntityType) -> object:
    parent_entity = None
    if entity_type == EntityType.course:
        parent_entity = Course.find_by_id(entity_id)
        if not parent_entity:
            raise CourseIdNotFoundException([str(entity_id)])
    elif entity_type == EntityType.lesson:
        parent_entity = Lesson.find_by_id(entity_id)
        if not parent_entity:
            raise LessonIdNotFoundException([str(entity_id)])
    elif entity_type == EntityType.comment:
        parent_entity = Comment.find_by_id(entity_id)
        if not parent_entity:
            raise CommentIdNotFoundException([str(entity_id)])
    else:
        raise EntityTypeNotSupportedException([entity_type.value])
    return parent_entity
