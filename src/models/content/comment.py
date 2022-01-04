from datetime import datetime

from sqlalchemy import Column, INT, DateTime
from sqlalchemy.dialects.postgresql import TEXT, ENUM

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
    content = Column(TEXT, nullable=False)
    likes = Column(INT, default=0)
    dislikes = Column(INT, default=0)
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
    def find_by_parent_id(parent_id: int, parent_type: EntityType) -> 'List[Comment]':
        return services.db.session.query(Comment).filter_by(parent_id=parent_id, parent_type=parent_type).all()

    @staticmethod
    def search_in_content(search_string) -> 'List[Comment]':
        return services.db.session.query(Comment).filter(Comment.content.contains(search_string)).all()

    @staticmethod
    def delete_by_id(id):
        return services.db.session.query(Comment).filter_by(id=id).delete()
