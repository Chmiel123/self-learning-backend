import datetime
from typing import List

from sqlalchemy import Column, INT, ForeignKey, DateTime, DECIMAL

from src.services import services
from src.utils.postgres_serializer_mixing import PostgresSerializerMixin


class PremiumTime(services.db.Base, PostgresSerializerMixin):
    __tablename__ = 'premium_time'
    __table_args__ = {'schema': 'account'}

    account_id = Column(INT, ForeignKey('account.account.id'), primary_key=True, nullable=False, index=True)
    end_date = Column(DateTime)

    def save_to_db(self):
        services.db.session.add(self)
        services.db.session.commit()

    @staticmethod
    def find_by_account_id(account_id: int) -> 'PremiumTime':
        return services.db.session.query(PremiumTime).filter_by(account_id=account_id).first()
