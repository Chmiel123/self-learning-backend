from typing import Dict, List

from src.logic import account_logic
from src.models import EntityType, get_comment_parent_entity
from src.models.account.account import Account
from src.models.content.lesson import Lesson
from src.models.content.comment import Comment
from src.models.system.entity_status import EntityStatus
from src.services import services
from src.utils import modify
from src.utils.exceptions import CommentIdNotFoundException, NotAuthorizedException, LessonIdNotFoundException, \
    CommentMaxDepthReachedException


def get_comments_for_parent(parent_id: int, parent_type: int, page_number: int, page_size: int)\
        -> Dict[str, List[Dict[str, str]]]:
    comments = Comment.find_by_parent_id(parent_id, EntityType(parent_type), page_number, page_size)
    return {
        'comments': [x.to_dict() for x in comments]
    }


def create_or_update(comment_dict: dict) -> Comment:
    current_account = account_logic.get_current_account()
    if comment_dict['id']:
        comment = Comment.find_by_id(comment_dict['id'])
        if comment:
            parent = get_comment_parent_entity(comment.parent_id, comment.parent_type)
            admin_privilege = account_logic.get_current_admin_privilege(current_account, parent.language_id)
            if current_account.id == comment.author_id or admin_privilege:
                comment = _update(comment, comment_dict, current_account)
                return comment.to_dict()
            else:
                raise NotAuthorizedException()
        else:
            raise CommentIdNotFoundException([comment_dict['id']])
    parent = get_comment_parent_entity(comment_dict['parent_id'], EntityType(comment_dict['parent_type']))
    course = _create(comment_dict, current_account, parent)
    return course.to_dict()


def delete(id: int):
    comment = Comment.find_by_id(id)
    if comment:
        current_account = account_logic.get_current_account()
        admin_privilege = account_logic.get_current_admin_privilege(current_account, comment.language_id)
        if current_account.id == comment.author_id or admin_privilege:
            comment.status = EntityStatus.deleted
            comment.save_to_db()
        else:
            raise NotAuthorizedException()
    else:
        raise CommentIdNotFoundException([str(id)])


def _create(comment_dict: dict, current_account: Account, parent):
    comment = Comment()
    comment.author_id = current_account.id
    comment.parent_id = comment_dict['parent_id']
    comment.parent_type = EntityType(comment_dict['parent_type'])
    comment.status = EntityStatus.active
    comment.content = comment_dict['content']
    comment.language_id = parent.language_id
    if isinstance(parent, Comment):
        comment.depth = parent.depth + 1
        if comment.depth > services.flask.config['MAX_COMMENT_DEPTH']:
            raise CommentMaxDepthReachedException()
        parent.replies += 1
        parent.save_to_db()
    comment.save_to_db()
    return comment


def _update(comment: Comment, comment_dict: dict, current_account: Account) -> Comment:
    changed = False
    changed = modify(comment, comment_dict['content'], 'content', changed)
    if changed:
        comment.save_to_db()
    return comment
