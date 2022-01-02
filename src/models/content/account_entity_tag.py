from typing import List

from sqlalchemy import Column, INT, ForeignKey, BOOLEAN
from sqlalchemy.dialects.postgresql import ENUM

from src.models.system.entity_type import EntityType
from src.services import services
from src.utils.postgres_serializer_mixing import PostgresSerializerMixin


class AccountEntityTag(services.db.Base, PostgresSerializerMixin):
    __tablename__ = 'account_entity_tags'
    __table_args__ = {'schema': 'content'}

    account_id = Column(INT, ForeignKey('account.account.id', ondelete='CASCADE'), primary_key=True)
    entity_id = Column(INT, nullable=False, index=True, primary_key=True)
    entity_type = Column(ENUM(EntityType), nullable=False, primary_key=True)
    like = Column(BOOLEAN, default=False)
    dislike = Column(BOOLEAN, default=False)
    favorite = Column(BOOLEAN, default=False)
    in_progress = Column(BOOLEAN, default=False)
    completed = Column(BOOLEAN, default=False)

    def save_to_db(self):
        services.db.session.add(self)
        services.db.session.commit()

    def set_like(self, value: bool):
        self.like = value
        if value:
            self.dislike = False

    def set_dislike(self, value: bool):
        self.dislike = value
        if value:
            self.like = False

    def set_favorite(self, value: bool):
        self.favorite = value

    def set_in_progress(self, value: bool):
        self.in_progress = value
        if value:
            self.completed = False

    def set_completed(self, value: bool):
        self.completed = value
        if value:
            self.in_progress = False

    @staticmethod
    def find_by_account_id_and_entity_id(account_id: int, entity_id: int, entity_type: EntityType) \
            -> 'AccountEntityTag':
        return services.db.session.query(AccountEntityTag) \
            .filter_by(account_id=account_id, entity_id=entity_id, entity_type=entity_type).first()

    @staticmethod
    def find_by_account_id_and_entity_type(account_id: int, entity_type: EntityType, entity_id_start: int,
                                           entity_id_end: int) -> 'List[AccountEntityTag]':
        return services.db.session.query(AccountEntityTag) \
            .filter(AccountEntityTag.entity_id >= entity_id_start, AccountEntityTag.entity_id <= entity_id_end,
                    AccountEntityTag.account_id == account_id, AccountEntityTag.entity_type == entity_type, ) \
            .order_by(AccountEntityTag.entity_id).all()

    @staticmethod
    def find_by_account_id(account_id, entity_type: EntityType) -> 'List[AccountEntityTag]':
        return services.db.session.query(AccountEntityTag) \
            .filter_by(account_id=account_id, entity_type=entity_type).all()

    @staticmethod
    def find_by_entity_id(entity_id, entity_type: EntityType) -> 'List[AccountEntityTag]':
        return services.db.session.query(AccountEntityTag) \
            .filter_by(entity_id=entity_id, entity_type=entity_type).all()

    @staticmethod
    def delete_by_account_id_and_entity_id(account_id: int, entity_id: int, entity_type: EntityType):
        return services.db.session.query(AccountEntityTag) \
            .filter_by(account_id=account_id, entity_id=entity_id, entity_type=entity_type).delete()
