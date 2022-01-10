import datetime
import random
import string

from sqlalchemy import Column, ForeignKey, DateTime, INT
from sqlalchemy.dialects.postgresql import TEXT

from src.services import services
from src.utils.postgres_serializer_mixing import PostgresSerializerMixin


class EmailVerification(services.db.Base, PostgresSerializerMixin):
    __tablename__ = 'email_verification'
    __table_args__ = {'schema': 'account'}

    account_id = Column(INT, ForeignKey('account.account.id', ondelete='CASCADE'), primary_key=True, unique=True,
                        nullable=False, index=True)
    email = Column(TEXT, nullable=False, unique=True, index=True)
    verification_key = Column(TEXT, nullable=False, index=True, unique=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, account_id: int, email: str):
        self.account_id = account_id
        self.email = email
        self.verification_key = ''.join(
            random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(20))

    def save_to_db(self):
        services.db.session.add(self)
        services.db.session.commit()

    @staticmethod
    def find_by_account_id(account_id) -> 'EmailVerification':
        return services.db.session.query(EmailVerification).filter_by(account_id=account_id).first()

    @staticmethod
    def find_by_verification_key(verification_key: str) -> 'EmailVerification':
        return services.db.session.query(EmailVerification).filter_by(verification_key=verification_key).first()

    @staticmethod
    def find_by_email(email) -> 'EmailVerification':
        return services.db.session.query(EmailVerification).filter_by(email=email).first()

    @staticmethod
    def delete_by_account_id(account_id):
        return services.db.session.query(EmailVerification).filter_by(account_id=account_id).delete()

    @staticmethod
    def delete_by_email(email):
        return services.db.session.query(EmailVerification).filter_by(email=email).delete()
