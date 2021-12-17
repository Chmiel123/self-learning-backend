from datetime import datetime, timedelta

from src.models.account.email_verification import EmailVerification
from src.models.account.password_reset import PasswordReset
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


def verify_email(verification_key: str) -> bool:
    found_email_verification = EmailVerification.find_by_verification_key(verification_key)
    if found_email_verification:
        found_account = Account.find_by_id(found_email_verification.account_id)
        max_hours = services.flask.config['EMAIL_VERIFICATION_HOURS']
        if found_email_verification.created_date + timedelta(hours=max_hours) > datetime.utcnow():
            found_account.email = found_email_verification.email
            EmailVerification.delete_by_account_id(found_account.id)
            return True
        else:
            raise ErrorException(ErrorCode.EMAIL_VERIFICATION_EXPIRED, [], 'Verification expired')
    else:
        raise ErrorException(ErrorCode.EMAIL_COULD_NOT_BE_VERIFIED, [], 'Email could not be verified')


def generate_password_reset(email: str) -> PasswordReset:
    found_account = Account.find_by_email(email)
    if not found_account:
        found_email_verification = EmailVerification.find_by_email(email)
        if found_email_verification:
            found_account = Account.find_by_id(found_email_verification.account_id)
    if not found_account:
        raise ErrorException(ErrorCode.USER_EMAIL_NOT_FOUND, [], 'User with email doesn\'t exist')
    PasswordReset.delete_by_account_id(found_account.id)
    password_reset = PasswordReset(found_account.id)
    password_reset.save_to_db()
    services.email.send_password_reset_email(email, password_reset)
    return password_reset


def verify_password_reset(verification_key: str, new_password: str) -> bool:
    found_password_reset = PasswordReset.find_by_verify_key(verification_key)
    if not found_password_reset:
        raise ErrorException(ErrorCode.PASSWORD_RESET_VERIFICATION_KEY_NOT_FOUND, [verification_key],
                             f'Invalid verification key: {verification_key}')
    max_hours = services.flask.config['PASSWORD_RESET_HOURS']
    if found_password_reset.created_date + timedelta(hours=max_hours) > datetime.utcnow():
        found_account = Account.find_by_id(found_password_reset.account_id)
        if not found_account:
            raise ErrorException(ErrorCode.USER_ID_NOT_FOUND, [found_password_reset.account_id],
                                 f'User with id {found_password_reset.account_id} not found')
        found_account.set_password(new_password)
        found_account.save_to_db()
        return True
    else:
        raise ErrorException(ErrorCode.PASSWORD_RESET_EXPIRED, [], 'Verification expired')

