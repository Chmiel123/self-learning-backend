from __future__ import annotations

from datetime import datetime
import enum

from sqlalchemy import Column, INT, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import TEXT, ENUM
from sqlalchemy.orm import relationship

from src.services import services
from src.utils.postgres_serializer_mixing import PostgresSerializerMixin


class Category(services.db.Base, PostgresSerializerMixin):
    __tablename__ = 'category'
    __table_args__ = {'schema': 'system'}

    id = Column(INT, primary_key=True, unique=True, nullable=False)
    name = Column(TEXT, nullable=False, unique=True, index=True)
    content = Column(TEXT, nullable=False)
    target_language_id = Column(INT, ForeignKey('system.language.id', ondelete='CASCADE'), nullable=False,
                                primary_key=True)
    created_date = Column(DateTime, default=datetime.utcnow)

    target_language = relationship("Language")

    def __init__(self, name: str, content: str):
        self.name = name
        self.content = content

    def save_to_db(self):
        services.db.session.add(self)
        services.db.session.commit()

    @staticmethod
    def find_by_id(id: int) -> 'Category':
        return services.db.session.query(Category).filter_by(id=id).first()

    @staticmethod
    def search_in_content(search_string) -> 'Category':
        return services.db.session.query(Category).filter(Category.content.contains(search_string)).all()

    @staticmethod
    def delete_by_id(id):
        return services.db.session.query(Category).filter_by(id=id).delete()
