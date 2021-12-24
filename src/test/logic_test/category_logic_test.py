from src.logic import category_logic
from src.models.content.category import Category
from src.models.system.language import Language
from src.test.base_test import BaseTest
from src.utils.exceptions import ErrorException


class CategoryLogicTest(BaseTest):
    def setUp(self):
        super().setUp()
        Language('en', 'english', 'english').save_to_db()

    def test_get_all_categories_for_language(self):
        category1 = Category('a', 'a is a category', 1)
        category1.save_to_db()
        category2 = Category('b', 'b is a category', 1)
        category2.save_to_db()

        found_categories = category_logic.get_all_categories_for_language('en')
        self.assertEqual(category1.name, found_categories['categories'][0]['name'])
        self.assertEqual(category2.name, found_categories['categories'][1]['name'])

    def test_language_not_found(self):
        category1 = Category('a', 'a is a category', 1)
        category1.save_to_db()
        category2 = Category('b', 'b is a category', 1)
        category2.save_to_db()

        self.assertRaises(ErrorException, category_logic.get_all_categories_for_language, 'es')

    def test_create(self):
        category_logic.create_or_update({
            'id': None,
            'name': 'a',
            'content': 'a is a category',
            'language_id': 1
        })
        found_categories = category_logic.get_all_categories_for_language('en')
        self.assertEqual('a', found_categories['categories'][0]['name'])

    def test_update(self):
        category_logic.create_or_update({
            'id': None,
            'name': 'a',
            'content': 'a is a category',
            'language_id': 1
        })
        found_categories = category_logic.get_all_categories_for_language('en')
        self.assertEqual('a', found_categories['categories'][0]['name'])
        category_logic.create_or_update({
            'id': 1,
            'name': 'b',
            'content': 'b is a category',
            'language_id': 1
        })
        found_categories = category_logic.get_all_categories_for_language('en')
        self.assertEqual('b is a category', found_categories['categories'][0]['content'])

    def test_update_id_not_found(self):
        category_logic.create_or_update({
            'id': None,
            'name': 'a',
            'content': 'a is a category',
            'language_id': 1
        })
        found_categories = category_logic.get_all_categories_for_language('en')
        self.assertEqual('a', found_categories['categories'][0]['name'])
        self.assertRaises(ErrorException, category_logic.create_or_update, {
            'id': 2,
            'name': 'b',
            'content': 'b is a category',
            'language_id': 1
        })
