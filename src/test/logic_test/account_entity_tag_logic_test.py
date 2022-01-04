from src.logic import account_entity_tag_logic
from src.models.content.account_entity_tag import AccountEntityTag
from src.models.content.category import Category
from src.models.content.category_course_link import CategoryCourseLink
from src.models.content.comment import Comment
from src.models.content.course import Course
from src.models.content.lesson import Lesson
from src.models.system.entity_status import EntityStatus
from src.models.system.entity_type import EntityType
from src.test.base_with_context_test import BaseWithContextTest
from src.utils.exceptions import AccountEntityTagIdNotFoundException, CourseIdNotFoundException, \
    LessonIdNotFoundException, CommentIdNotFoundException, EntityTypeNotSupportedException, \
    AccountEntityTagLikeDislikeBothTrueException, AccountEntityTagInProgressCompletedBothTrueException


class AccountEntityTagLogicTest(BaseWithContextTest):
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
        CategoryCourseLink(1, 1).save_to_db()
        lesson = Lesson()
        lesson.name = 'c'
        lesson.content = 'c is a lesson'
        lesson.language_id = 1
        lesson.author_id = 1
        lesson.course_id = course1.id
        lesson.save_to_db()
        comment = Comment()
        comment.content = 'this is a comment'
        comment.author_id = 1
        comment.parent_id = 1
        comment.parent_type = EntityType.course
        comment.save_to_db()

    def test_create_question(self):
        account_entity_tag_logic.create_or_update({
            "entity_id": 1,
            "entity_type": 2,
            "like": "true",
            "dislike": "false",
            "favorite": "true",
            "in_progress": "true",
            "completed": "false"
        })
        tag = AccountEntityTag.find_by_account_id_and_entity_id(1, 1, EntityType.course)
        self.assertEqual(1, tag.entity_id)
        self.assertEqual(EntityType.course, tag.entity_type)
        self.assertEqual(True, tag.like)
        self.assertEqual(False, tag.dislike)
        self.assertEqual(True, tag.favorite)
        self.assertEqual(True, tag.in_progress)
        self.assertEqual(False, tag.completed)
        account_entity_tag_logic.create_or_update({
            "entity_id": 1,
            "entity_type": 3,
            "like": "true",
            "dislike": "false",
            "favorite": "true",
            "in_progress": "true",
            "completed": "false"
        })
        tag = AccountEntityTag.find_by_account_id_and_entity_id(1, 1, EntityType.lesson)
        self.assertEqual(1, tag.entity_id)
        self.assertEqual(EntityType.lesson, tag.entity_type)
        self.assertEqual(True, tag.like)
        self.assertEqual(False, tag.dislike)
        self.assertEqual(True, tag.favorite)
        self.assertEqual(True, tag.in_progress)
        self.assertEqual(False, tag.completed)
        account_entity_tag_logic.create_or_update({
            "entity_id": 1,
            "entity_type": 4,
            "like": "true",
            "dislike": "false",
            "favorite": "true",
            "in_progress": "true",
            "completed": "false"
        })
        tag = AccountEntityTag.find_by_account_id_and_entity_id(1, 1, EntityType.comment)
        self.assertEqual(1, tag.entity_id)
        self.assertEqual(EntityType.comment, tag.entity_type)
        self.assertEqual(True, tag.like)
        self.assertEqual(False, tag.dislike)
        self.assertEqual(True, tag.favorite)
        self.assertEqual(True, tag.in_progress)
        self.assertEqual(False, tag.completed)

    def test_create_update_question(self):
        account_entity_tag_logic.create_or_update({
            "entity_id": 1,
            "entity_type": 2,
            "like": "true",
            "dislike": "false",
            "favorite": "true",
            "in_progress": "true",
            "completed": "false"
        })
        tag = AccountEntityTag.find_by_account_id_and_entity_id(1, 1, EntityType.course)
        self.assertEqual(1, tag.entity_id)
        self.assertEqual(EntityType.course, tag.entity_type)
        self.assertEqual(True, tag.like)
        self.assertEqual(False, tag.dislike)
        self.assertEqual(True, tag.favorite)
        self.assertEqual(True, tag.in_progress)
        self.assertEqual(False, tag.completed)
        account_entity_tag_logic.create_or_update({
            "entity_id": 1,
            "entity_type": 2,
            "like": "true",
            "dislike": "false",
            "favorite": "true",
            "in_progress": "true",
            "completed": "false"
        })
        tag = AccountEntityTag.find_by_account_id_and_entity_id(1, 1, EntityType.course)
        self.assertEqual(1, tag.entity_id)
        self.assertEqual(EntityType.course, tag.entity_type)
        self.assertEqual(True, tag.like)
        self.assertEqual(False, tag.dislike)
        self.assertEqual(True, tag.favorite)
        self.assertEqual(True, tag.in_progress)
        self.assertEqual(False, tag.completed)
        account_entity_tag_logic.create_or_update({
            "entity_id": 1,
            "entity_type": 2,
            "like": "false",
            "dislike": "true",
            "favorite": "false",
            "in_progress": "false",
            "completed": "true"
        })
        tag = AccountEntityTag.find_by_account_id_and_entity_id(1, 1, EntityType.course)
        self.assertEqual(1, tag.entity_id)
        self.assertEqual(EntityType.course, tag.entity_type)
        self.assertEqual(False, tag.like)
        self.assertEqual(True, tag.dislike)
        self.assertEqual(False, tag.favorite)
        self.assertEqual(False, tag.in_progress)
        self.assertEqual(True, tag.completed)
        account_entity_tag_logic.create_or_update({
            "entity_id": 1,
            "entity_type": 2,
            "like": "true",
            "dislike": "false",
            "favorite": "false",
            "in_progress": "false",
            "completed": "true"
        })
        tag = AccountEntityTag.find_by_account_id_and_entity_id(1, 1, EntityType.course)
        self.assertEqual(1, tag.entity_id)
        self.assertEqual(EntityType.course, tag.entity_type)
        self.assertEqual(True, tag.like)
        self.assertEqual(False, tag.dislike)
        self.assertEqual(False, tag.favorite)
        self.assertEqual(False, tag.in_progress)
        self.assertEqual(True, tag.completed)

        account_entity_tag_logic.create_or_update({
            "entity_id": 1,
            "entity_type": 3,
            "like": "true",
            "dislike": "false",
            "favorite": "true",
            "in_progress": "true",
            "completed": "false"
        })
        tag = AccountEntityTag.find_by_account_id_and_entity_id(1, 1, EntityType.lesson)
        self.assertEqual(1, tag.entity_id)
        self.assertEqual(EntityType.lesson, tag.entity_type)
        self.assertEqual(True, tag.like)
        self.assertEqual(False, tag.dislike)
        self.assertEqual(True, tag.favorite)
        self.assertEqual(True, tag.in_progress)
        self.assertEqual(False, tag.completed)
        account_entity_tag_logic.create_or_update({
            "entity_id": 1,
            "entity_type": 3,
            "like": "false",
            "dislike": "true",
            "favorite": "true",
            "in_progress": "true",
            "completed": "false"
        })
        tag = AccountEntityTag.find_by_account_id_and_entity_id(1, 1, EntityType.lesson)
        self.assertEqual(1, tag.entity_id)
        self.assertEqual(EntityType.lesson, tag.entity_type)
        self.assertEqual(False, tag.like)
        self.assertEqual(True, tag.dislike)
        self.assertEqual(True, tag.favorite)
        self.assertEqual(True, tag.in_progress)
        self.assertEqual(False, tag.completed)

        account_entity_tag_logic.create_or_update({
            "entity_id": 1,
            "entity_type": 4,
            "like": "true",
            "dislike": "false",
            "favorite": "true",
            "in_progress": "true",
            "completed": "false"
        })
        tag = AccountEntityTag.find_by_account_id_and_entity_id(1, 1, EntityType.comment)
        self.assertEqual(1, tag.entity_id)
        self.assertEqual(EntityType.comment, tag.entity_type)
        self.assertEqual(True, tag.like)
        self.assertEqual(False, tag.dislike)
        self.assertEqual(True, tag.favorite)
        self.assertEqual(True, tag.in_progress)
        self.assertEqual(False, tag.completed)
        account_entity_tag_logic.create_or_update({
            "entity_id": 1,
            "entity_type": 4,
            "like": "false",
            "dislike": "true",
            "favorite": "true",
            "in_progress": "true",
            "completed": "false"
        })
        tag = AccountEntityTag.find_by_account_id_and_entity_id(1, 1, EntityType.comment)
        self.assertEqual(1, tag.entity_id)
        self.assertEqual(EntityType.comment, tag.entity_type)
        self.assertEqual(False, tag.like)
        self.assertEqual(True, tag.dislike)
        self.assertEqual(True, tag.favorite)
        self.assertEqual(True, tag.in_progress)
        self.assertEqual(False, tag.completed)

    def test_get_account_entity_tags_for_entities(self):
        account_entity_tag_logic.create_or_update({
            "entity_id": 1,
            "entity_type": 2,
            "like": "false",
            "dislike": "true",
            "favorite": "true",
            "in_progress": "true",
            "completed": "false"
        })
        result = account_entity_tag_logic.get_account_entity_tags_for_entities('1-100', EntityType.course.value)
        self.assertEqual(False, result['account_entity_tags'][0]['like'])
        self.assertEqual(True, result['account_entity_tags'][0]['dislike'])

    def test_delete(self):
        account_entity_tag_logic.create_or_update({
            "entity_id": 1,
            "entity_type": 2,
            "like": "true",
            "dislike": "false",
            "favorite": "true",
            "in_progress": "true",
            "completed": "false"
        })
        account_entity_tag_logic.delete({
            "entity_id": 1,
            "entity_type": 2,
        })
        tag = AccountEntityTag.find_by_account_id_and_entity_id(1, 1, EntityType.course)
        self.assertIsNone(tag)
        self.assertRaises(AccountEntityTagIdNotFoundException, account_entity_tag_logic.delete, {
            "entity_id": 1,
            "entity_type": 2,
        })

    def test_id_not_found(self):
        self.assertRaises(CourseIdNotFoundException,
                          account_entity_tag_logic.create_or_update, {
                                "entity_id": 2,
                                "entity_type": 2,
                                "like": "true",
                                "dislike": "false",
                                "favorite": "true",
                                "in_progress": "true",
                                "completed": "false"
                            })
        self.assertRaises(LessonIdNotFoundException,
                          account_entity_tag_logic.create_or_update, {
                                "entity_id": 2,
                                "entity_type": 3,
                                "like": "true",
                                "dislike": "false",
                                "favorite": "true",
                                "in_progress": "true",
                                "completed": "false"
                            })
        self.assertRaises(CommentIdNotFoundException,
                          account_entity_tag_logic.create_or_update, {
                                "entity_id": 2,
                                "entity_type": 4,
                                "like": "true",
                                "dislike": "false",
                                "favorite": "true",
                                "in_progress": "true",
                                "completed": "false"
                            })
        self.assertRaises(EntityTypeNotSupportedException,
                          account_entity_tag_logic.create_or_update, {
                                "entity_id": 2,
                                "entity_type": 1,
                                "like": "true",
                                "dislike": "false",
                                "favorite": "true",
                                "in_progress": "true",
                                "completed": "false"
                            })
        self.assertRaises(AccountEntityTagIdNotFoundException, account_entity_tag_logic.delete, {
            "entity_id": 1,
            "entity_type": 2,
        })

    def test_double_true_fields(self):
        self.assertRaises(AccountEntityTagLikeDislikeBothTrueException,
                          account_entity_tag_logic.create_or_update, {
                                "entity_id": 1,
                                "entity_type": 2,
                                "like": "true",
                                "dislike": "true",
                                "favorite": "true",
                                "in_progress": "true",
                                "completed": "false"
                            })
        self.assertRaises(AccountEntityTagInProgressCompletedBothTrueException,
                          account_entity_tag_logic.create_or_update, {
                                "entity_id": 1,
                                "entity_type": 2,
                                "like": "true",
                                "dislike": "false",
                                "favorite": "true",
                                "in_progress": "true",
                                "completed": "true"
                            })

    def test_number_of_likes_and_dislikes(self):
        account_entity_tag_logic.create_or_update({
            "entity_id": 1,
            "entity_type": 2,
            "like": "false",
            "dislike": "true",
            "favorite": "true",
            "in_progress": "true",
            "completed": "false"
        })
        course = Course.find_by_id(1)
        self.assertEqual(0, course.likes)
        self.assertEqual(1, course.dislikes)
        account_entity_tag_logic.create_or_update({
            "entity_id": 1,
            "entity_type": 2,
            "like": "true",
            "dislike": "false",
            "favorite": "true",
            "in_progress": "true",
            "completed": "false"
        })
        course = Course.find_by_id(1)
        self.assertEqual(1, course.likes)
        self.assertEqual(0, course.dislikes)

        account_entity_tag_logic.create_or_update({
            "entity_id": 1,
            "entity_type": 3,
            "like": "true",
            "dislike": "false",
            "favorite": "true",
            "in_progress": "true",
            "completed": "false"
        })
        lesson = Lesson.find_by_id(1)
        self.assertEqual(1, lesson.likes)
        self.assertEqual(0, lesson.dislikes)
        account_entity_tag_logic.create_or_update({
            "entity_id": 1,
            "entity_type": 3,
            "like": "false",
            "dislike": "true",
            "favorite": "true",
            "in_progress": "true",
            "completed": "false"
        })
        lesson = Lesson.find_by_id(1)
        self.assertEqual(0, lesson.likes)
        self.assertEqual(1, lesson.dislikes)
