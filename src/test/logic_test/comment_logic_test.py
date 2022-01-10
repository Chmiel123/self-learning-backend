from src.logic import comment_logic
from src.models import Course, Comment, EntityType, Lesson
from src.models.content.category import Category
from src.models.content.category_course_link import CategoryCourseLink
from src.models.system.entity_status import EntityStatus
from src.test.base_with_context_test import BaseWithContextTest
from src.utils.exceptions import CourseIdNotFoundException, CommentIdNotFoundException, EntityTypeNotSupportedException, \
    LessonIdNotFoundException, NotAuthorizedException, CommentMaxDepthReachedException


class CommentLogicTest(BaseWithContextTest):
    def setUp(self):
        super().setUp()
        category1 = Category()
        category1.name = 'a'
        category1.content = 'a is a category'
        category1.status = EntityStatus.active
        category1.language_id = 1
        category1.can_add_courses = True
        category1.author_id = 1
        category1.save_to_db()
        course1 = Course()
        course1.name = 'b'
        course1.content = 'b is a course'
        course1.status = EntityStatus.active
        course1.language_id = 1
        course1.author_id = 1
        course1.save_to_db()
        category_course_link = CategoryCourseLink()
        category_course_link.category_id = 1
        category_course_link.course_id = 1
        category_course_link.save_to_db()
        lesson = Lesson()
        lesson.name = 'c'
        lesson.content = 'c is a lesson'
        lesson.language_id = 1
        lesson.author_id = 1
        lesson.course_id = course1.id
        lesson.save_to_db()

    def test_create_comment(self):
        comment_logic.create_or_update({
            "id": None,
            "parent_id": 1,
            "parent_type": 2,
            "content": "This is a comment"
        })
        comment_logic.create_or_update({
            "id": None,
            "parent_id": 1,
            "parent_type": 4,
            "content": "This is a sub comment"
        })
        comment = Comment.find_by_id(1)
        self.assertEqual(1, comment.id)
        self.assertEqual(1, comment.parent_id)
        self.assertEqual(EntityType.course, comment.parent_type)
        self.assertEqual("This is a comment", comment.content)
        self.assertEqual(EntityStatus.active, comment.status)
        self.assertEqual(0, comment.likes)
        self.assertEqual(0, comment.dislikes)
        self.assertEqual(1, comment.depth)
        self.assertEqual(1, comment.replies)
        self.assertEqual(1, comment.language_id)
        comment = Comment.find_by_id(2)
        self.assertEqual(2, comment.id)
        self.assertEqual(1, comment.parent_id)
        self.assertEqual(EntityType.comment, comment.parent_type)
        self.assertEqual("This is a sub comment", comment.content)
        self.assertEqual(EntityStatus.active, comment.status)
        self.assertEqual(0, comment.likes)
        self.assertEqual(0, comment.dislikes)
        self.assertEqual(2, comment.depth)
        self.assertEqual(0, comment.replies)
        self.assertEqual(1, comment.language_id)

    def test_create_update_comment(self):
        comment_logic.create_or_update({
            "id": None,
            "parent_id": 1,
            "parent_type": 3,
            "content": "This is a comment"
        })
        comment_logic.create_or_update({
            "id": 1,
            "content": "This is an edited comment"
        })
        comment_logic.create_or_update({
            "id": 1,
            "content": "This is an edited comment"
        })
        comment = Comment.find_by_id(1)
        self.assertEqual(1, comment.id)
        self.assertEqual(1, comment.parent_id)
        self.assertEqual(EntityType.lesson, comment.parent_type)
        self.assertEqual("This is an edited comment", comment.content)
        self.assertEqual(EntityStatus.active, comment.status)
        self.assertEqual(0, comment.likes)
        self.assertEqual(0, comment.dislikes)
        self.assertEqual(1, comment.depth)
        self.assertEqual(0, comment.replies)
        self.assertEqual(1, comment.language_id)

    def test_get_comments_for_entity(self):
        comment_logic.create_or_update({
            "id": None,
            "parent_id": 1,
            "parent_type": 2,
            "content": "This is a comment 1"
        })
        comment_logic.create_or_update({
            "id": None,
            "parent_id": 1,
            "parent_type": 2,
            "content": "This is a comment 2"
        })
        result = comment_logic.get_comments_for_parent(1, 2, 1, 100)
        self.assertEqual(1, result['comments'][0]['id'])
        self.assertEqual("This is a comment 1", result['comments'][0]['content'])
        self.assertEqual(2, result['comments'][1]['id'])
        self.assertEqual("This is a comment 2", result['comments'][1]['content'])

    def test_delete(self):
        comment_logic.create_or_update({
            "id": None,
            "parent_id": 1,
            "parent_type": 2,
            "content": "This is a comment"
        })
        comment_logic.delete(1)
        comment = Comment.find_by_id(1)
        self.assertEqual(1, comment.id)
        self.assertEqual(1, comment.parent_id)
        self.assertEqual(EntityType.course, comment.parent_type)
        self.assertEqual("This is a comment", comment.content)
        self.assertEqual(EntityStatus.deleted, comment.status)
        self.assertEqual(0, comment.likes)
        self.assertEqual(0, comment.dislikes)
        self.assertEqual(1, comment.depth)
        self.assertEqual(0, comment.replies)
        self.assertEqual(1, comment.language_id)

    def test_id_not_found(self):
        self.assertRaises(CourseIdNotFoundException,
                          comment_logic.create_or_update, {
                              "id": None,
                              "parent_id": 2,
                              "parent_type": 2,
                              "content": "This is a comment"
                          })
        self.assertRaises(LessonIdNotFoundException,
                          comment_logic.create_or_update, {
                              "id": None,
                              "parent_id": 2,
                              "parent_type": 3,
                              "content": "This is a comment"
                          })
        self.assertRaises(CommentIdNotFoundException,
                          comment_logic.create_or_update, {
                              "id": None,
                              "parent_id": 2,
                              "parent_type": 4,
                              "content": "This is a comment"
                          })
        self.assertRaises(CommentIdNotFoundException,
                          comment_logic.create_or_update, {
                              "id": 1,
                              "content": "This is a comment"
                          })
        self.assertRaises(EntityTypeNotSupportedException,
                          comment_logic.create_or_update, {
                              "id": None,
                              "parent_id": 2,
                              "parent_type": 1,
                              "content": "This is a comment"
                          })
        self.assertRaises(CommentIdNotFoundException, comment_logic.delete, 2)

    def test_not_authorized(self):
        comment_logic.create_or_update({
            "id": None,
            "parent_id": 1,
            "parent_type": 2,
            "content": "This is a comment"
        })
        self.login_as_user()
        self.assertRaises(NotAuthorizedException,
                          comment_logic.create_or_update, {
                              "id": 1,
                              "parent_id": 2,
                              "parent_type": 4,
                              "content": "This is an edited comment"
                          })
        self.assertRaises(NotAuthorizedException, comment_logic.delete, 1)

    def test_max_depth_reached(self):
        comment_logic.create_or_update({
            "id": None,
            "parent_id": 1,
            "parent_type": 2,
            "content": "This is a comment"
        })
        comment_logic.create_or_update({
            "id": None,
            "parent_id": 1,
            "parent_type": 4,
            "content": "This is a sub comment"
        })
        self.assertRaises(CommentMaxDepthReachedException,
                          comment_logic.create_or_update, {
                              "id": None,
                              "parent_id": 2,
                              "parent_type": 4,
                              "content": "This is a sub comment"
                          })
