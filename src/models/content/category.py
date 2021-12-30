from datetime import datetime
from typing import List

from sqlalchemy import Column, INT, DateTime, ForeignKey, BOOLEAN, SMALLINT
from sqlalchemy.dialects.postgresql import TEXT, ENUM

from src.models.system.entity_status import EntityStatus
from src.models.system.language import Language
from src.services import services
from src.utils.postgres_serializer_mixing import PostgresSerializerMixin


class Category(services.db.Base, PostgresSerializerMixin):
    __tablename__ = 'category'
    __table_args__ = {'schema': 'content'}

    id = Column(INT, primary_key=True, unique=True, nullable=False)
    parent_id = Column(INT, ForeignKey('content.category.id'), nullable=True, index=True)
    author_id = Column(INT, nullable=True, index=True)
    name = Column(TEXT, nullable=False, index=True)
    content = Column(TEXT, nullable=False)
    status = Column(ENUM(EntityStatus), nullable=False, default=EntityStatus.draft)
    can_add_courses = Column(BOOLEAN, default=False)
    nr_active_courses = Column(INT, default=0)
    language_id = Column(SMALLINT, ForeignKey('system.language.id'), nullable=False)
    created_date = Column(DateTime, default=datetime.utcnow)

    def __init__(self):
        pass

    def save_to_db(self):
        services.db.session.add(self)
        services.db.session.commit()

    @staticmethod
    def find_all() -> 'List[Category]':
        return services.db.session.query(Category).all()

    @staticmethod
    def find_by_id(id: int) -> 'Category':
        return services.db.session.query(Category).filter_by(id=id).first()

    @staticmethod
    def find_by_language_id(language_id: int) -> 'List[Category]':
        return services.db.session.query(Category).filter_by(language_id=language_id).all()

    @staticmethod
    def search_in_content(search_string) -> 'List[Category]':
        return services.db.session.query(Category).filter(Category.content.contains(search_string)).all()

    @staticmethod
    def delete_by_id(id):
        return services.db.session.query(Category).filter_by(id=id).delete()
