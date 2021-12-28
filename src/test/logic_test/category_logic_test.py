from src.logic import category_logic
from src.models.content.category import Category
from src.models.system.entity_status import EntityStatus
from src.test.base_with_context_test import BaseWithContextTest
from src.utils.exceptions import LanguageCodeNotFoundException, AdminPrivilegeRequiredException, \
    CategoryIdNotFoundException


class CategoryLogicTest(BaseWithContextTest):
    def test_get_all_categories_for_language(self):
        category1 = Category()
        category1.name = 'a'
        category1.content = 'a is a category'
        category1.language_id = 1
        category1.save_to_db()
        category2 = Category()
        category2.name = 'b'
        category2.content = 'b is a category'
        category2.language_id = 1
        category2.save_to_db()

        found_categories = category_logic.get_all_categories_for_language('en')
        self.assertEqual(category1.name, found_categories['categories'][0]['name'])
        self.assertEqual(category2.name, found_categories['categories'][1]['name'])

    def test_language_not_found(self):
        category1 = Category()
        category1.name = 'a'
        category1.content = 'a is a category'
        category1.language_id = 1
        category1.save_to_db()
        category2 = Category()
        category2.name = 'b'
        category2.content = 'b is a category'
        category2.language_id = 1
        category2.save_to_db()

        self.assertRaises(LanguageCodeNotFoundException, category_logic.get_all_categories_for_language, 'es')

    def test_create(self):
        category_logic.create_or_update({
            'id': None,
            'name': 'a',
            'content': 'a is a category',
            'language_id': 1,
            'parent_id': None,
            'can_add_courses': True
        })
        found_categories = category_logic.get_all_categories_for_language('en')
        self.assertEqual('a', found_categories['categories'][0]['name'])

    def test_create_or_update_no_admin_privilege(self):
        self.login_as_user()
        self.assertRaises(AdminPrivilegeRequiredException, category_logic.create_or_update, {
            'id': None,
            'name': 'a',
            'content': 'a is a category',
            'language_id': 1,
            'parent_id': None
        })

    def test_update(self):
        category_logic.create_or_update({
            'id': None,
            'name': 'a',
            'content': 'a is a category',
            'language_id': 1,
            'status': 2,
            'parent_id': None,
            'can_add_courses': True
        })
        found_categories = category_logic.get_all_categories_for_language('en')
        self.assertEqual('a', found_categories['categories'][0]['name'])
        category_logic.create_or_update({
            'id': 1,
            'name': 'b',
            'content': 'b is a category',
            'language_id': 1,
            'status': 2,
            'parent_id': None,
            'can_add_courses': True
        })
        found_categories = category_logic.get_all_categories_for_language('en')
        self.assertEqual('b is a category', found_categories['categories'][0]['content'])

    def test_update_id_not_found(self):
        category_logic.create_or_update({
            'id': None,
            'name': 'a',
            'content': 'a is a category',
            'language_id': 1,
            'parent_id': None,
            'can_add_courses': True
        })
        found_categories = category_logic.get_all_categories_for_language('en')
        self.assertEqual('a', found_categories['categories'][0]['name'])
        self.assertRaises(CategoryIdNotFoundException, category_logic.create_or_update, {
            'id': 2,
            'name': 'b',
            'content': 'b is a category',
            'language_id': 1
        })

    def test_delete(self):
        category_logic.create_or_update({
            'id': None,
            'name': 'a',
            'content': 'a is a category',
            'language_id': 1,
            'parent_id': None,
            'can_add_courses': True
        })
        found_categories = category_logic.get_all_categories_for_language('en')
        self.assertEqual('a', found_categories['categories'][0]['name'])
        self.assertRaises(CategoryIdNotFoundException, category_logic.delete, 2)
        category_logic.delete(1)
        found_categories = category_logic.get_all_categories_for_language('en')
        self.assertEqual(EntityStatus.deleted.value, found_categories['categories'][0]['status'])

    def test_delete_no_admin_privilege(self):
        category_logic.create_or_update({
            'id': None,
            'name': 'a',
            'content': 'a is a category',
            'language_id': 1,
            'parent_id': None,
            'can_add_courses': True
        })
        self.login_as_user()
        self.assertRaises(AdminPrivilegeRequiredException, category_logic.delete, 1)
