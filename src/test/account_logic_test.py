import unittest

from src.logic import account_logic
from src.models.account.account import Account
from src.test.base_test import BaseTest
from src.util.exceptions import InvalidInputDataException


class AccountLogicTest(BaseTest):
    def test_create_account_with_password(self):
        account = account_logic.create_account_with_password('john', 'john@example.com', 'pass')

        found_account = Account.find_by_username('john')
        self.assertEqual(account, found_account)

    def test_create_account_with_password_duplicate_username(self):
        account = account_logic.create_account_with_password('john', 'john@example.com', 'pass')
        self.assertRaises(InvalidInputDataException,
                          account_logic.create_account_with_password,
                          'john', 'john2@example.com', 'pass')

    def test_create_account_with_password_duplicate_email(self):
        account = account_logic.create_account_with_password('john', 'john@example.com', 'pass')
        self.assertRaises(InvalidInputDataException,
                          account_logic.create_account_with_password,
                          'bill', 'john@example.com', 'pass')


if __name__ == '__main__':
    unittest.main()
