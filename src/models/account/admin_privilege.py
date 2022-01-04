from typing import List

from sqlalchemy import Column, INT, ForeignKey, SMALLINT

from src.services import services
from src.utils.postgres_serializer_mixing import PostgresSerializerMixin


class AdminPrivilege(services.db.Base, PostgresSerializerMixin):
    __tablename__ = 'admin_privilege'
    __table_args__ = {'schema': 'account'}

    id = Column(INT, primary_key=True, unique=True, nullable=False)
    account_id = Column(INT, ForeignKey('account.account.id', ondelete='CASCADE'), nullable=False)
    language_id = Column(SMALLINT, ForeignKey('system.language.id'), nullable=False)
    strength = Column(INT, nullable=False)

    def save_to_db(self):
        services.db.session.add(self)
        services.db.session.commit()

    @staticmethod
    def find_by_id(id: int) -> 'AdminPrivilege':
        return services.db.session.query(AdminPrivilege).filter_by(id=id).first()

    @staticmethod
    def find_by_account_id(account_id: int) -> 'List[AdminPrivilege]':
        return services.db.session.query(AdminPrivilege).filter_by(account_id=account_id).all()

    @staticmethod
    def find_by_account_id_and_language_id(account_id: int, language_id: int) -> 'AdminPrivilege':
        return services.db.session.query(AdminPrivilege)\
            .filter_by(account_id=account_id, language_id=language_id).first()

    @staticmethod
    def delete_by_account_id_and_language_id(account_id: int, language_id: int):
        return services.db.session.query(AdminPrivilege)\
            .filter_by(account_id=account_id, language_id=language_id).delete()

    @staticmethod
    def delete_by_id(id):
        return services.db.session.query(AdminPrivilege).filter_by(id=id).delete()
