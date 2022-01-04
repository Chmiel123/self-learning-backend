import datetime
import random
import string

from sqlalchemy import Column, ForeignKey, DateTime, INT
from sqlalchemy.dialects.postgresql import TEXT

from src.services import services
from src.utils.postgres_serializer_mixing import PostgresSerializerMixin


class PasswordReset(services.db.Base, PostgresSerializerMixin):
    __tablename__ = 'password_reset'
    __table_args__ = {'schema': 'account'}

    account_id = Column(INT, ForeignKey('account.account.id', ondelete='CASCADE'), primary_key=True,
                        unique=True, nullable=False, index=True)
    verification_key = Column(TEXT, nullable=False, index=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, account_id: int):
        self.account_id = account_id
        self.verification_key = ''.join(
            random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(20))

    def save_to_db(self):
        services.db.session.add(self)
        services.db.session.commit()

    @staticmethod
    def find_by_verify_key(verification_key: str):
        return services.db.session.query(PasswordReset).filter_by(verification_key=verification_key).first()

    @staticmethod
    def find_by_account_id(account_id):
        return services.db.session.query(PasswordReset).filter_by(account_id=account_id).first()

    @staticmethod
    def delete_by_account_id(account_id):
        return services.db.session.query(PasswordReset).filter_by(account_id=account_id).delete()
