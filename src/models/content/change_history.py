from datetime import datetime
from typing import List

from sqlalchemy import Column, INT, DateTime
from sqlalchemy.dialects.postgresql import TEXT, ENUM

from src.models.system.entity_status import EntityStatus
from src.models.system.entity_type import EntityType
from src.services import services
from src.utils.postgres_serializer_mixing import PostgresSerializerMixin


class ChangeHistory(services.db.Base, PostgresSerializerMixin):
    __tablename__ = 'change_history'
    __table_args__ = {'schema': 'content'}

    id = Column(INT, primary_key=True, unique=True, nullable=False)
    author_id = Column(INT, nullable=True, index=True)
    parent_id = Column(INT, nullable=True, index=True)
    parent_type = Column(ENUM(EntityType), nullable=False)
    name = Column(TEXT, nullable=False, index=True)
    content = Column(TEXT, nullable=False)
    status = Column(ENUM(EntityStatus), nullable=False, default=EntityStatus.draft)
    created_date = Column(DateTime, default=datetime.utcnow)

    def __init__(self, author_id: int, parent_id: int, parent_type: EntityType, name: str, content: str,
                 status: EntityStatus):
        self.author_id = author_id
        self.parent_id = parent_id
        self.parent_type = parent_type
        self.name = name
        self.content = content
        self.status = status

    def save_to_db(self):
        services.db.session.add(self)
        services.db.session.commit()

    @staticmethod
    def find_by_id(id: int) -> 'ChangeHistory':
        return services.db.session.query(ChangeHistory).filter_by(id=id).first()

    @staticmethod
    def find_by_parent_id(parent_id: int, parent_type) -> 'List[ChangeHistory]':
        return services.db.session.query(ChangeHistory).filter_by(parent_id=parent_id, parent_type=parent_type).all()

    @staticmethod
    def delete_by_id(id):
        return services.db.session.query(ChangeHistory).filter_by(id=id).delete()
