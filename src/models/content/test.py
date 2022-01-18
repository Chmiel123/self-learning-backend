from datetime import datetime
from typing import List

from sqlalchemy import Column, INT, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import ENUM

from src.models.system.test_status import TestStatus
from src.services import services
from src.utils.postgres_serializer_mixing import PostgresSerializerMixin


class Test(services.db.Base, PostgresSerializerMixin):
    __tablename__ = 'test'
    __table_args__ = {'schema': 'content'}

    id = Column(INT, primary_key=True, unique=True, nullable=False, index=True)
    test_id = Column(INT, ForeignKey('content.lesson.id'), nullable=False, index=True)
    solver_id = Column(INT, nullable=False, index=True)
    status = Column(ENUM(TestStatus), nullable=False, default=TestStatus.in_progress)
    created_date = Column(DateTime, default=datetime.utcnow)

    def save_to_db(self):
        services.db.session.add(self)
        services.db.session.commit()

    @staticmethod
    def find_by_id(id: int) -> 'Test':
        return services.db.session.query(Test).filter_by(id=id).first()

    @staticmethod
    def find_by_test_id(test_id: int) -> 'List[Test]':
        return services.db.session.query(Test).filter_by(test_id=test_id).all()

    @staticmethod
    def find_by_solver_id(solver_id: int) -> 'List[Test]':
        return services.db.session.query(Test).filter_by(solver_id=solver_id).all()

    @staticmethod
    def find_by_test_id_and_solver_id(test_id: int, solver_id: int) -> 'List[Test]':
        return services.db.session.query(Test).filter_by(test_id=test_id, solver_id=solver_id).all()

    @staticmethod
    def delete_by_id(id):
        return services.db.session.query(Test).filter_by(id=id).delete()
