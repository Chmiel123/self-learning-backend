from src.util.enum import Enum


class ErrorCode:
    USER_USERNAME_ALREADY_EXISTS = Enum('user_username_already_exists')
    USER_EMAIL_ALREADY_EXISTS = Enum('user_email_already_exists')
    WRONG_CREDENTIALS = Enum('wrong_credentials')
    DUPLICATE_EMAIL = Enum('duplicate_email')







