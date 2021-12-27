import unittest
from datetime import datetime, timedelta

from src.logic import account_logic
from src.models.account.account import Account
from src.models.account.email_verification import EmailVerification
from src.models.account.password_reset import PasswordReset
from src.test.base_test import BaseTest
from src.utils.exceptions import UserNameAlreadyExistsException, \
    UserEmailAlreadyExistsException, WrongCredentialsException, EmailIsTheSameException, DuplicateEmailException, \
    EmailVerificationKeyNotFoundException, EmailVerificationExpiredException, UserEmailNotFoundException, \
    PasswordResetVerificationKeyNotFoundException, PasswordResetExpiredException


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
        account_logic.create_account_with_password('john', 'john@example.com', 'pass')
        self.assertRaises(UserNameAlreadyExistsException,
                          account_logic.create_account_with_password,
                          'john', 'john2@example.com', 'pass')

    def test_create_account_with_password_duplicate_email(self):
        account = account_logic.create_account_with_password('john', 'john@example.com', 'pass')
        self.assertRaises(UserEmailAlreadyExistsException,
                          account_logic.create_account_with_password,
                          'bill', 'john@example.com', 'pass')
        account.email = 'john@example.com'
        account.save_to_db()
        self.assertRaises(UserEmailAlreadyExistsException,
                          account_logic.create_account_with_password,
                          'bill', 'john@example.com', 'pass')

    def test_create_account_and_login(self):
        account = account_logic.create_account_with_password('john', 'john@example.com', 'pass')
        logged_in_account = account_logic.login('john', 'pass')
        self.assertEqual(account, logged_in_account)
        # look in email verification
        logged_in_account = account_logic.login('john@example.com', 'pass')
        self.assertEqual(account, logged_in_account)
        # look in account
        account.email = 'john@example.com'
        account.save_to_db()
        logged_in_account = account_logic.login('john@example.com', 'pass')
        self.assertEqual(account, logged_in_account)
        self.assertRaises(WrongCredentialsException,
                          account_logic.login,
                          'bill', 'pass')

    def test_generate_verification_email(self):
        # generated by create account with password
        account = account_logic.create_account_with_password('john', 'john@example.com', 'pass')
        found_email_verification = EmailVerification.find_by_account_id(account.id)
        self.assertIsNotNone(found_email_verification)
        # resend email
        account_logic.generate_email_verification(account, 'john@example.com')
        found_email_verification_2 = EmailVerification.find_by_account_id(account.id)
        self.assertNotEqual(found_email_verification.verification_key,
                            found_email_verification_2.verification_key)
        # already verified
        account.email = 'john@example.com'
        account.save_to_db()
        self.assertRaises(EmailIsTheSameException,
                          account_logic.generate_email_verification,
                          account, 'john@example.com')
        # generate new email
        account_logic.generate_email_verification(account, 'jill@example.com')
        found_email_verification_3 = EmailVerification.find_by_account_id(account.id)
        self.assertNotEqual(found_email_verification.verification_key,
                            found_email_verification_3.verification_key)
        # another account has email verification
        account2 = account_logic.create_account_with_password('bill', 'bill@example.com', 'pass')
        self.assertRaises(DuplicateEmailException,
                          account_logic.generate_email_verification,
                          account, 'bill@example.com')
        # another account has email
        account2.email = 'bill@example.com'
        account2.save_to_db()
        self.assertRaises(DuplicateEmailException,
                          account_logic.generate_email_verification,
                          account, 'bill@example.com')

    def test_verify_email(self):
        account = account_logic.create_account_with_password('john', 'john@example.com', 'pass')
        # bad verification key
        self.assertRaises(EmailVerificationKeyNotFoundException,
                          account_logic.verify_email,
                          'aaaaaaaaaaa')
        found_email_verification = EmailVerification.find_by_account_id(account.id)
        result = account_logic.verify_email(found_email_verification.verification_key)
        self.assertTrue(result)
        found_account = Account.find_by_username('john')
        self.assertEqual('john@example.com', found_account.email)

    def test_verify_email_verification_expired(self):
        account_logic.create_account_with_password('john', 'john@example.com', 'pass')
        found_account = Account.find_by_username('john')
        found_ev = EmailVerification.find_by_account_id(found_account.id)
        found_ev.created_date = datetime.utcnow() - timedelta(hours=9999)
        self.assertRaises(EmailVerificationExpiredException,
                          account_logic.verify_email,
                          found_ev.verification_key)

    def test_generate_password_reset(self):
        account = account_logic.create_account_with_password('john', 'john@example.com', 'pass')
        self.assertRaises(UserEmailNotFoundException,
                          account_logic.generate_password_reset,
                          'john2@example.com')
        password_reset = account_logic.generate_password_reset('john@example.com')
        self.assertEqual(password_reset.account_id, account.id)
        account.email = 'john@example.com'
        account.save_to_db()
        password_reset = account_logic.generate_password_reset('john@example.com')
        self.assertEqual(password_reset.account_id, account.id)

    def test_verify_password_reset(self):
        account = account_logic.create_account_with_password('john', 'john@example.com', 'pass')
        first_password = account.password
        password_reset = account_logic.generate_password_reset('john@example.com')
        # bad verification key
        self.assertRaises(PasswordResetVerificationKeyNotFoundException,
                          account_logic.verify_password_reset,
                          'aaaaaaaaaaa', 'pass2')
        result = account_logic.verify_password_reset(password_reset.verification_key, 'pass2')
        found_account = Account.find_by_username('john')
        second_password = found_account.password
        self.assertTrue(result)
        self.assertNotEqual(first_password, second_password)

    def test_verify_password_reset_verification_expired(self):
        account = account_logic.create_account_with_password('john', 'john@example.com', 'pass')
        account_logic.generate_password_reset('john@example.com')
        found_pr = PasswordReset.find_by_account_id(account.id)
        found_pr.created_date = datetime.utcnow() - timedelta(hours=9999)
        self.assertRaises(PasswordResetExpiredException,
                          account_logic.verify_password_reset,
                          found_pr.verification_key, 'pass2')


if __name__ == '__main__':
    unittest.main()
