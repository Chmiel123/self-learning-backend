from datetime import datetime
import enum

from sqlalchemy import Column, INT, DateTime, BOOLEAN
from sqlalchemy.dialects.postgresql import TEXT, ENUM

from src.models.system.entity_type import EntityType
from src.services import services
from src.utils.postgres_serializer_mixing import PostgresSerializerMixin


class Comment(services.db.Base, PostgresSerializerMixin):
    __tablename__ = 'comment'
    __table_args__ = {'schema': 'system'}

    id = Column(INT, primary_key=True, unique=True, nullable=False)
    author_id = Column(INT, nullable=True, index=True)
    parent_id = Column(INT, nullable=True, index=True)
    parent_type = Column(ENUM(EntityType), nullable=False, default=EntityType.lesson)
    content = Column(TEXT, nullable=False)
    created_date = Column(DateTime, default=datetime.utcnow)

    def __init__(self, author_id: int, parent_id: int, parent_type: EntityType, content: str):
        self.author_id = author_id
        self.parent_id = parent_id
        self.parent_type = parent_type
        self.content = content

    def save_to_db(self):
        services.db.session.add(self)
        services.db.session.commit()

    @staticmethod
    def find_by_id(id: int) -> 'Comment':
        return services.db.session.query(Comment).filter_by(id=id).first()

    @staticmethod
    def find_by_author_id(author_id: int) -> 'Comment':
        return services.db.session.query(Comment).filter_by(author_id=author_id).all()

    @staticmethod
    def find_by_parent_id(parent_id: int, parent_type: EntityType) -> 'Comment':
        return services.db.session.query(Comment).filter_by(parent_id=parent_id, parent_type=parent_type).all()

    @staticmethod
    def search_in_content(search_string) -> 'Comment':
        return services.db.session.query(Comment).filter(Comment.content.contains(search_string)).all()

    @staticmethod
    def delete_by_id(id):
        return services.db.session.query(Comment).filter_by(id=id).delete()
