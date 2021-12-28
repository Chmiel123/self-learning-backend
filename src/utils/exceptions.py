from typing import List


class SelfLearningBackendException(Exception):
    pass


class ErrorException(SelfLearningBackendException):
    def __init__(self, parameters: List[str] = [], default_message='Error occurred'):
        self.parameters = parameters
        self.default_message = default_message
        super().__init__()


class WarningException(SelfLearningBackendException):
    def __init__(self, parameters: List[str] = [], default_message='Warning'):
        self.parameters = parameters
        self.default_message = default_message
        super().__init__()


class WrongCredentialsException(ErrorException):
    def __init__(self, parameters: List[str] = []):
        super().__init__(parameters)
        self.default_message = 'Wrong credentials'
class NotAuthorizedException(ErrorException):
    def __init__(self, parameters: List[str] = []):
        super().__init__(parameters)
        self.default_message = 'Not authorized'
class AdminPrivilegeRequiredException(ErrorException):
    def __init__(self, parameters: List[str] = []):
        super().__init__(parameters)
        self.default_message = 'Admin privilege required'
class UserNameAlreadyExistsException(ErrorException):
    def __init__(self, parameters: List[str] = []):
        super().__init__(parameters)
        self.default_message = 'User {} already exists'
class UserEmailAlreadyExistsException(ErrorException):
    def __init__(self, parameters: List[str] = []):
        super().__init__(parameters)
        self.default_message = 'User with email {} already exists'
class UserIdNotFoundException(ErrorException):
    def __init__(self, parameters: List[str] = []):
        super().__init__(parameters)
        self.default_message = 'User with id {} not found'
class UserNameNotFoundException(ErrorException):
    def __init__(self, parameters: List[str] = []):
        super().__init__(parameters)
        self.default_message = 'User with name {} not found'
class UserEmailNotFoundException(ErrorException):
    def __init__(self, parameters: List[str] = []):
        super().__init__(parameters)
        self.default_message = 'User with email doesn\'t exist'
class UserIdOrNameNotFoundException(ErrorException):
    def __init__(self, parameters: List[str] = []):
        super().__init__(parameters)
        self.default_message = 'User with id {} or name {} not found'
class DuplicateEmailException(ErrorException):
    def __init__(self, parameters: List[str] = []):
        super().__init__(parameters)
        self.default_message = 'User with email {} already exists'
class EmailVerificationExpiredException(ErrorException):
    def __init__(self, parameters: List[str] = []):
        super().__init__(parameters)
        self.default_message = 'Email verification expired'
class EmailVerificationKeyNotFoundException(ErrorException):
    def __init__(self, parameters: List[str] = []):
        super().__init__(parameters)
        self.default_message = 'Email verification key {} not found'
class PasswordResetExpiredException(ErrorException):
    def __init__(self, parameters: List[str] = []):
        super().__init__(parameters)
        self.default_message = 'Password reset expired'
class PasswordResetVerificationKeyNotFoundException(ErrorException):
    def __init__(self, parameters: List[str] = []):
        super().__init__(parameters)
        self.default_message = 'Password reset verification key {} not found'
class LanguageCodeNotFoundException(ErrorException):
    def __init__(self, parameters: List[str] = []):
        super().__init__(parameters)
        self.default_message = 'Language code {} not found'
class CategoryIdNotFoundException(ErrorException):
    def __init__(self, parameters: List[str] = []):
        super().__init__(parameters)
        self.default_message = 'Category with id {} not found'
class CourseIdNotFoundException(ErrorException):
    def __init__(self, parameters: List[str] = []):
        super().__init__(parameters)
        self.default_message = 'Course with id {} not found'


class EmailIsTheSameException(WarningException):
    def __init__(self, parameters: List[str] = []):
        super().__init__(parameters)
        self.default_message = 'User has already verified email {}'

