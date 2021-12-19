from datetime import datetime

from sqlalchemy import Column, INT, DateTime, ForeignKey, BOOLEAN, UniqueConstraint, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import TEXT, ENUM

from src.models.system.entity_type import EntityType
from src.services import services
from src.utils.postgres_serializer_mixing import PostgresSerializerMixin


class AccountEntityTags(services.db.Base, PostgresSerializerMixin):
    __tablename__ = 'reaction'
    __table_args__ = {'schema': 'system'}

    account_id = Column(INT, ForeignKey('account.account.id', ondelete='CASCADE'), primary_key=True)
    entity_id = Column(INT, nullable=False, index=True, primary_key=True)
    entity_type = Column(ENUM(EntityType), nullable=False, primary_key=True)
    like = Column(BOOLEAN, default=False)
    dislike = Column(BOOLEAN, default=False)
    favorite = Column(BOOLEAN, default=False)
    in_progress = Column(BOOLEAN, default=False)
    completed = Column(BOOLEAN, default=False)

    def __init__(self, account_id: int, entity_id: int, entity_type: EntityType):
        self.account_id = account_id
        self.entity_id = entity_id
        self.entity_type = entity_type

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
    def find_by_account_id_and_entity_id(account_id: int, entity_id: int, entity_type: EntityType)\
            -> 'AccountEntityTags':
        return services.db.session.query(AccountEntityTags)\
            .filter_by(account_id=account_id, entity_id=entity_id, entity_type=entity_type).first()

    @staticmethod
    def find_by_account_id(account_id, entity_type: EntityType) -> 'AccountEntityTags':
        return services.db.session.query(AccountEntityTags)\
            .filter_by(account_id=account_id, entity_type=entity_type).all()

    @staticmethod
    def find_by_entity_id(entity_id, entity_type: EntityType) -> 'AccountEntityTags':
        return services.db.session.query(AccountEntityTags)\
            .filter_by(entity_id=entity_id, entity_type=entity_type).all()

    @staticmethod
    def delete_by_account_id_and_entity_id(account_id: int, entity_id: int, entity_type: EntityType):
        return services.db.session.query(AccountEntityTags)\
            .filter_by(account_id=account_id, entity_id=entity_id, entity_type=entity_type).delete()
