from datetime import datetime
from typing import List

from sqlalchemy import Column, INT, DateTime, ForeignKey, SMALLINT
from sqlalchemy.dialects.postgresql import TEXT, ENUM

from src.models.system.entity_status import EntityStatus
from src.services import services
from src.utils.postgres_serializer_mixing import PostgresSerializerMixin


class Question(services.db.Base, PostgresSerializerMixin):
    __tablename__ = 'quiz_question'
    __table_args__ = {'schema': 'content'}

    id = Column(INT, primary_key=True, unique=True, nullable=False)
    lesson_id = Column(INT, ForeignKey('content.lesson.id'), nullable=False, index=True)
    order_begin = Column(SMALLINT)
    order_end = Column(SMALLINT)
    question = Column(TEXT, nullable=False)
    available_answers = Column(TEXT, nullable=True)
    correct_answers = Column(TEXT, nullable=False)
    solution = Column(TEXT, nullable=True)

    def save_to_db(self):
        services.db.session.add(self)
        services.db.session.commit()

    @staticmethod
    def find_by_id(id: int) -> 'Question':
        return services.db.session.query(Question).filter_by(id=id).first()

    @staticmethod
    def find_by_lesson_id(lesson_id: int) -> 'List[Question]':
        return services.db.session.query(Question).filter_by(lesson_id=lesson_id).all()

    @staticmethod
    def delete_by_id(id):
        return services.db.session.query(Question).filter_by(id=id).delete()
