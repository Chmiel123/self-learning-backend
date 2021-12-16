from src.models.account.email_verification import EmailVerification
from src.util.error_code import ErrorCode
from src.util.exceptions import ErrorException, WarningException
from src.models.account.account import Account
from src.util.warning_code import WarningCode
from src.services import services


def create_account_with_password(username: str, email: str, password: str) -> Account:
    if Account.find_by_username(username):
        raise ErrorException(ErrorCode.USER_USERNAME_ALREADY_EXISTS, [username], f'User {username} already exists')
    if Account.find_by_email(email):
        raise ErrorException(ErrorCode.USER_EMAIL_ALREADY_EXISTS, [email], f'User with email {email} already exists')
    if EmailVerification.find_by_email(email):
        raise ErrorException(ErrorCode.USER_EMAIL_ALREADY_EXISTS, [email], f'User with email {email} already exists')

    new_account = Account(username, password)
    new_account.save_to_db()

    email_verification = EmailVerification(new_account.id, email)
    email_verification.save_to_db()
    services.email.send_email_verification_email(email_verification)

    return new_account


def login(username_or_email: str, password: str) -> Account:
    current_account = Account.find_by_username(username_or_email)

    if current_account:
        if Account.verify_hash(password, current_account.password):
            return current_account

    current_account = Account.find_by_email(username_or_email)
    if current_account:
        if Account.verify_hash(password, current_account.password):
            return current_account

    current_email_verification = EmailVerification.find_by_email(username_or_email)
    if current_email_verification:
        current_account = Account.find_by_id(current_email_verification.account_id)
        if current_account:
            if Account.verify_hash(password, current_account.password):
                return current_account

    else:
        raise ErrorException(ErrorCode.WRONG_CREDENTIALS, [], 'Wrong credentials.')


def generate_email_verification(account: Account, email: str) -> EmailVerification:
    found_account = Account.find_by_email(email)
    if found_account:
        if found_account.id == account.id:
            raise WarningException(WarningCode.EMAIL_IS_THE_SAME, [email], f'User has already verified email {email}')
        else:
            raise ErrorException(ErrorCode.DUPLICATE_EMAIL, [email], f'User with email {email} already exists.')
    found_email_verification = EmailVerification.find_by_email(email)
    if found_email_verification:
        if found_email_verification.account_id == account.id:
            EmailVerification.delete_by_account_id(account.id)
            email_verification = EmailVerification(account.id, email)
            email_verification.save_to_db()
            services.email.send_email_verification_email(email_verification)
            return email_verification
        else:
            raise ErrorException(ErrorCode.DUPLICATE_EMAIL, [email], f'User with email {email} already exists.')
    found_email_verification = EmailVerification.find_by_account_id(account.id)
    if found_email_verification:
        EmailVerification.delete_by_account_id(account.id)
    email_verification = EmailVerification(account.id, email)
    email_verification.save_to_db()
    services.email.send_email_verification_email(email_verification)
    return email_verification
