from src.models.account.email_verification import EmailVerification
from src.util.error_code import ErrorCodes
from src.util.exceptions import ErrorException
from src.models.account.account import Account


def create_account_with_password(username: str, email: str, password: str) -> Account:
    if Account.find_by_username(username):
        raise ErrorException(ErrorCodes.USER_USERNAME_ALREADY_EXISTS, [username], f'User {username} already exists')
    if Account.find_by_email(email):
        raise ErrorException(ErrorCodes.USER_EMAIL_ALREADY_EXISTS, [email],f'User with email {email} already exists')
    if EmailVerification.find_by_email(email):
        raise ErrorException(ErrorCodes.USER_EMAIL_ALREADY_EXISTS, [email],f'User with email {email} already exists')

    new_account = Account(username, password)
    new_account.save_to_db()

    email_verification = EmailVerification(new_account.id, email)
    email_verification.save_to_db()

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

    else:
        raise ErrorException(ErrorCodes.WRONG_CREDENTIALS, [], 'Wrong credentials.')

# def generate_email_verification(email: str) -> EmailVerification:
#     if account_email.verified:
#         raise IMException('Account already verified')
#     EmailVerification.delete_by_email(account_email.email)
#
#     ev = EmailVerification(account_email.email)
#     ev.save_to_db()
#     return ev
