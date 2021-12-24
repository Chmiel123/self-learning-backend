from datetime import datetime
from typing import List

from sqlalchemy import Column, INT, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import TEXT

from src.services import services
from src.utils.postgres_serializer_mixing import PostgresSerializerMixin


class Category(services.db.Base, PostgresSerializerMixin):
    __tablename__ = 'category'
    __table_args__ = {'schema': 'content'}

    id = Column(INT, primary_key=True, unique=True, nullable=False)
    name = Column(TEXT, nullable=False, unique=True, index=True)
    content = Column(TEXT, nullable=False)
    nr_lesson_groups = Column(INT, default=0)
    language_id = Column(INT, ForeignKey('system.language.id'), nullable=False)
    created_date = Column(DateTime, default=datetime.utcnow)

    def __init__(self, name: str, content: str, language_id: int):
        self.name = name
        self.content = content
        self.language_id = language_id

    def save_to_db(self):
        services.db.session.add(self)
        services.db.session.commit()

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'content': self.content,
            'nr_lesson_groups': self.nr_lesson_groups,
            'created_date': str(self.created_date)
        }

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
