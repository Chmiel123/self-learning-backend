import unittest

from src.logic import account_logic
from src.models.account.account import Account
from src.models.account.email_verification import EmailVerification
from src.test.base_test import BaseTest
from src.util.exceptions import ErrorException


class AccountLogicTest(BaseTest):
    def test_create_account_with_password(self):
        account = account_logic.create_account_with_password('john', 'john@example.com', 'pass')

        found_account: Account = Account.find_by_username('john')
        self.assertEqual(account, found_account)
        self.assertEqual('john', found_account.name)
        self.assertIsNone(found_account.email)
        found_email_verification: EmailVerification = EmailVerification.find_by_email('john@example.com')
        self.assertIsNotNone(found_email_verification)

    def test_find_none(self):
        found_account = Account.find_by_username('bill')
        self.assertIsNone(found_account)

    def test_create_account_with_password_duplicate_username(self):
        account = account_logic.create_account_with_password('john', 'john@example.com', 'pass')
        self.assertRaises(ErrorException,
                          account_logic.create_account_with_password,
                          'john', 'john2@example.com', 'pass')

    def test_create_account_with_password_duplicate_email(self):
        account = account_logic.create_account_with_password('john', 'john@example.com', 'pass')
        self.assertRaises(ErrorException,
                          account_logic.create_account_with_password,
                          'bill', 'john@example.com', 'pass')


if __name__ == '__main__':
    unittest.main()
