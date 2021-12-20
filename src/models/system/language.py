from __future__ import annotations

from datetime import datetime
import enum

from sqlalchemy import Column, INT, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import TEXT, ENUM
from sqlalchemy.orm import relationship

from src.models.system.entity_type import EntityType
from src.services import services
from src.utils.postgres_serializer_mixing import PostgresSerializerMixin


class Language(services.db.Base, PostgresSerializerMixin):
    __tablename__ = 'language'
    __table_args__ = {'schema': 'system'}

    id = Column(INT, primary_key=True, unique=False, nullable=False)
    # ISO 639-1 Code
    code = Column(String(5), nullable=False)

    def __init__(self, code: str):
        self.code = code

    def save_to_db(self):
        services.db.session.add(self)
        services.db.session.commit()

    @staticmethod
    def find_by_code(code: code) -> 'Language':
        return services.db.session.query(Language).filter_by(code=code).first()

    @staticmethod
    def find_by_id(id: int) -> 'Language':
        return services.db.session.query(Language).filter_by(id=id).first()
