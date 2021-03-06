from flask import Flask

from src.models.account.email_verification import EmailVerification
from src.models.account.password_reset import PasswordReset


class EmailService:
    def __init__(self, flask: Flask):
        self.flask = flask

    def send_email_verification_email(self, email_verification: EmailVerification):
        # TODO: send email verification email
        pass

    def send_password_reset_email(self, email: str, password_reset: PasswordReset):
        # TODO: send email verification email
        pass


class FakeEmailService(EmailService):
    def send_email_verification_email(self, email_verification: EmailVerification):
        # print(f'TO: {email_verification.email}, verification key: {email_verification.verification_key}.')
        pass

    def send_password_reset_email(self, email: str, password_reset: PasswordReset):
        pass
