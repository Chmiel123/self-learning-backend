from datetime import datetime
from typing import List

from sqlalchemy import Column, INT, DateTime, ForeignKey, SMALLINT, FLOAT
from sqlalchemy.dialects.postgresql import TEXT, ENUM

from src.models.system.entity_status import EntityStatus
from src.services import services
from src.utils.postgres_serializer_mixing import PostgresSerializerMixin


class Answer(services.db.Base, PostgresSerializerMixin):
    __tablename__ = 'answer'
    __table_args__ = {'schema': 'content'}

    id = Column(INT, primary_key=True, unique=True, nullable=False)
    test_id = Column(INT, ForeignKey('content.test.id'), nullable=False, index=True)
    question_id = Column(INT, ForeignKey('content.question.id'), nullable=False, index=True)
    order = Column(SMALLINT)
    student_answer = Column(TEXT)
    teacher_remark = Column(TEXT)
    points_earned = Column(FLOAT)

    def save_to_db(self):
        services.db.session.add(self)
        services.db.session.commit()

    @staticmethod
    def find_by_id(id: int) -> 'Answer':
        return services.db.session.query(Answer).filter_by(id=id).first()

    @staticmethod
    def find_by_solved_test_id(test_id: int) -> 'List[Answer]':
        return services.db.session.query(Answer).filter_by(test_id=test_id).all()

    @staticmethod
    def delete_by_id(id):
        return services.db.session.query(Answer).filter_by(id=id).delete()
