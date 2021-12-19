from __future__ import annotations

from datetime import datetime
import enum

from sqlalchemy import Column, INT, DateTime, ForeignKey, UniqueConstraint, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import TEXT, ENUM
from sqlalchemy.orm import relationship

from src.services import services
from src.utils.postgres_serializer_mixing import PostgresSerializerMixin


class CategoryCategoryLink(services.db.Base, PostgresSerializerMixin):
    __tablename__ = 'category_category_link'
    __table_args__ = {'schema': 'system'}

    top_id = Column(INT, ForeignKey('system.category.id'), primary_key=True)
    bottom_id = Column(INT, ForeignKey('system.category.id'), primary_key=True)

    def __init__(self, top_id: int, bottom_id: int):
        self.top_id = top_id
        self.bottom_id = bottom_id

    def save_to_db(self):
        services.db.session.add(self)
        services.db.session.commit()

    @staticmethod
    def find_by_top_id_bottom_id(top_id: int, bottom_id: int):
        return services.db.session.query(CategoryCategoryLink).filter_by(top_id=top_id, bottom_id=bottom_id).first()

    @staticmethod
    def find_by_top_id(top_id: int) -> 'CategoryCategoryLink':
        return services.db.session.query(CategoryCategoryLink).filter_by(top_id=top_id).all()

    @staticmethod
    def find_by_bottom_id(bottom_id: int) -> 'CategoryCategoryLink':
        return services.db.session.query(CategoryCategoryLink).filter_by(bottom_id=bottom_id).all()

    @staticmethod
    def delete_by_top_id_bottom_id(top_id: int, bottom_id: int):
        return services.db.session.query(CategoryCategoryLink).filter_by(top_id=top_id, bottom_id=bottom_id).delete()
