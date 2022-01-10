import datetime
from typing import List

from sqlalchemy import Column, INT, ForeignKey, DateTime, DECIMAL

from src.services import services
from src.utils.postgres_serializer_mixing import PostgresSerializerMixin


class FinancialTransaction(services.db.Base, PostgresSerializerMixin):
    __tablename__ = 'financial_transaction'
    __table_args__ = {'schema': 'account'}

    id = Column(INT, primary_key=True, unique=True, nullable=False)
    account_id = Column(INT, ForeignKey('account.account.id'), primary_key=True, nullable=False,
                        index=True)
    amount = Column(DECIMAL, nullable=False)
    date = Column(DateTime, default=datetime.datetime.utcnow)

    def save_to_db(self):
        services.db.session.add(self)
        services.db.session.commit()

    @staticmethod
    def find_by_id(id: int) -> 'FinancialTransaction':
        return services.db.session.query(FinancialTransaction).filter_by(id=id).first()

    @staticmethod
    def find_by_account_id(account_id) -> 'List[FinancialTransaction]':
        return services.db.session.query(FinancialTransaction).filter_by(account_id=account_id).all()
