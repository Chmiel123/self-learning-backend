from datetime import datetime, timedelta

from flask_jwt_extended import get_jwt_identity

from src.models.account.admin_privilege import AdminPrivilege
from src.models.account.email_verification import EmailVerification
from src.models.account.password_reset import PasswordReset
from src.utils.error_code import ErrorCode
from src.utils.exceptions import ErrorException, WarningException, UserNameAlreadyExistsException, \
    UserEmailAlreadyExistsException, UserEmailNotFoundException, UserIdNotFoundException, WrongCredentialsException, \
    DuplicateEmailException, EmailVerificationExpiredException, \
    EmailVerificationKeyNotFoundException, PasswordResetVerificationKeyNotFoundException, PasswordResetExpiredException, \
    EmailIsTheSameException, AdminPrivilegeRequiredException, UserNameNotFoundException
from src.models.account.account import Account
from src.utils.warning_code import WarningCode
from src.services import services


def create_account_with_password(username: str, email: str, password: str) -> Account:
    if Account.find_by_username(username):
        raise UserNameAlreadyExistsException([username])
    if Account.find_by_email(email):
        raise UserEmailAlreadyExistsException([email])
    if EmailVerification.find_by_email(email):
        raise UserEmailAlreadyExistsException([email])

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
        raise WrongCredentialsException()


def generate_email_verification(account: Account, email: str) -> EmailVerification:
    found_account = Account.find_by_email(email)
    if found_account:
        if found_account.id == account.id:
            raise EmailIsTheSameException([email])
        else:
            raise DuplicateEmailException([email])
    found_email_verification = EmailVerification.find_by_email(email)
    if found_email_verification:
        if found_email_verification.account_id == account.id:
            EmailVerification.delete_by_account_id(account.id)
            email_verification = EmailVerification(account.id, email)
            email_verification.save_to_db()
            services.email.send_email_verification_email(email_verification)
            return email_verification
        else:
            raise DuplicateEmailException([email])
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
            raise EmailVerificationExpiredException()
    else:
        raise EmailVerificationKeyNotFoundException(verification_key)


def generate_password_reset(email: str) -> PasswordReset:
    found_account = Account.find_by_email(email)
    if not found_account:
        found_email_verification = EmailVerification.find_by_email(email)
        if found_email_verification:
            found_account = Account.find_by_id(found_email_verification.account_id)
    if not found_account:
        raise UserEmailNotFoundException()
    PasswordReset.delete_by_account_id(found_account.id)
    password_reset = PasswordReset(found_account.id)
    password_reset.save_to_db()
    services.email.send_password_reset_email(email, password_reset)
    return password_reset


def verify_password_reset(verification_key: str, new_password: str) -> bool:
    found_password_reset = PasswordReset.find_by_verify_key(verification_key)
    if not found_password_reset:
        raise PasswordResetVerificationKeyNotFoundException([verification_key])
    max_hours = services.flask.config['PASSWORD_RESET_HOURS']
    if found_password_reset.created_date + timedelta(hours=max_hours) > datetime.utcnow():
        found_account = Account.find_by_id(found_password_reset.account_id)
        if not found_account:
            raise UserIdNotFoundException([found_password_reset.account_id])
        found_account.set_password(new_password)
        found_account.save_to_db()
        return True
    else:
        raise PasswordResetExpiredException()


def check_if_admin_privilege(language_id: int):
    current_account = get_current_account()
    admin_privilege = get_current_admin_privilege(current_account, language_id)
    if not admin_privilege:
        raise AdminPrivilegeRequiredException()
    return current_account


def get_current_account():
    current_user = get_jwt_identity()
    current_account = Account.find_by_username(current_user)
    if not current_account:
        raise UserNameNotFoundException([current_user])
    return current_account


def get_current_admin_privilege(current_account: Account, language_id: int):
    return AdminPrivilege.find_by_account_id_and_language_id(current_account.id, language_id)
