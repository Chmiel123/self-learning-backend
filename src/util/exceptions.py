from typing import List

from src.util.error_code import Enum


class SelfLearningBackendException(Exception):
    pass


class ErrorException(SelfLearningBackendException):
    def __init__(self, error_code: Enum, parameters: List[str] = [], default_message='Error occurred.'):
        self.error_code = error_code.value
        self.parameters = parameters
        self.default_message = default_message
        super().__init__()


class WarningException(SelfLearningBackendException):
    def __init__(self, warning_code: Enum, parameters: List[str] = [], default_message='Warning.'):
        self.warning_code = warning_code.value
        self.parameters = parameters
        self.default_message = default_message
        super().__init__()
