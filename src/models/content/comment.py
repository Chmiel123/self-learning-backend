from datetime import datetime
from typing import List

from sqlalchemy import Column, INT, DateTime, SMALLINT, ForeignKey
from sqlalchemy.dialects.postgresql import TEXT, ENUM

from src.models.system.entity_status import EntityStatus
from src.models.system.entity_type import EntityType
from src.services import services
from src.utils.postgres_serializer_mixing import PostgresSerializerMixin


class Comment(services.db.Base, PostgresSerializerMixin):
    __tablename__ = 'comment'
    __table_args__ = {'schema': 'content'}

    id = Column(INT, primary_key=True, unique=True, nullable=False, index=True)
    author_id = Column(INT, nullable=True, index=True)
    parent_id = Column(INT, nullable=True, index=True)
    parent_type = Column(ENUM(EntityType), nullable=False, index=True)
    status = Column(ENUM(EntityStatus), nullable=False, default=EntityStatus.active)
    content = Column(TEXT, nullable=False)
    likes = Column(INT, nullable=False, default=0)
    dislikes = Column(INT, nullable=False, default=0)
    depth = Column(SMALLINT, nullable=False, default=1)
    replies = Column(INT, nullable=False, default=0)
    language_id = Column(SMALLINT, ForeignKey('system.language.id', ondelete='CASCADE'), nullable=False)
    created_date = Column(DateTime, default=datetime.utcnow)

    def save_to_db(self):
        services.db.session.add(self)
        services.db.session.commit()

    @staticmethod
    def find_by_id(id: int) -> 'Comment':
        return services.db.session.query(Comment).filter_by(id=id).first()

    @staticmethod
    def find_by_author_id(author_id: int) -> 'List[Comment]':
        return services.db.session.query(Comment).filter_by(author_id=author_id).all()

    @staticmethod
    def find_by_parent_id(parent_id: int, parent_type: EntityType, page_number: int, page_size: int) -> 'List[Comment]':
        return services.db.session.query(Comment).filter_by(parent_id=parent_id, parent_type=parent_type)\
            .order_by(Comment.likes).limit(page_size).offset((page_number - 1) * page_size).all()

    @staticmethod
    def search_in_content(search_string) -> 'List[Comment]':
        return services.db.session.query(Comment).filter(Comment.content.contains(search_string)).all()

    @staticmethod
    def delete_by_id(id):
        return services.db.session.query(Comment).filter_by(id=id).delete()
