from src.utils.enum import Enum


class ErrorCode:
    USER_USERNAME_ALREADY_EXISTS = Enum('user_username_already_exists')
    USER_EMAIL_ALREADY_EXISTS = Enum('user_email_already_exists')
    USER_EMAIL_NOT_FOUND = Enum('user_email_not_found')
    USER_ID_NOT_FOUND = Enum('user_id_not_found')
    USER_NOT_FOUND = Enum('user_not_found')
    WRONG_CREDENTIALS = Enum('wrong_credentials')
    DUPLICATE_EMAIL = Enum('duplicate_email')
    EMAIL_VERIFICATION_EXPIRED = Enum('email_verification_expired')
    EMAIL_COULD_NOT_BE_VERIFIED = Enum('email_could_not_be_verified')
    PASSWORD_RESET_VERIFICATION_KEY_NOT_FOUND = Enum('password_reset_verification_key_not_found')
    PASSWORD_RESET_EXPIRED = Enum('password_reset_expired')
    LANGUAGE_CODE_NOT_FOUND = Enum('language_code_not_found')
    CATEGORY_ID_NOT_FOUND = Enum('category_not_not_found')




