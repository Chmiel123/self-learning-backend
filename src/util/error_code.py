
class Enum:
    def __init__(self, value):
        self.value = value


class ErrorCodes:
    USER_USERNAME_ALREADY_EXISTS = Enum('user_username_already_exists')
    USER_EMAIL_ALREADY_EXISTS = Enum('user_email_already_exists')
    WRONG_CREDENTIALS = Enum('wrong_credentials')
