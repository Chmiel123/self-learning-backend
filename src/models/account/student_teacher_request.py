from typing import List

from sqlalchemy import Column, INT, ForeignKey, BOOLEAN

from src.services import services
from src.utils.postgres_serializer_mixing import PostgresSerializerMixin


class StudentTeacherRequest(services.db.Base, PostgresSerializerMixin):
    __tablename__ = 'student_teacher_request'
    __table_args__ = {'schema': 'account'}

    teacher_id = Column(INT, ForeignKey('account.account.id'), primary_key=True, nullable=False, index=True)
    student_id = Column(INT, ForeignKey('account.account.id'), primary_key=True, nullable=False, index=True)
    teacher_accepted = Column(BOOLEAN, default=False)
    student_accepted = Column(BOOLEAN, default=False)

    def save_to_db(self):
        services.db.session.add(self)
        services.db.session.commit()

    @staticmethod
    def find_by_teacher_id_and_student_id(teacher_id: int, student_id: int) -> 'StudentTeacherRequest':
        return services.db.session.query(StudentTeacherRequest).filter_by(teacher_id=teacher_id, student_id=student_id)\
            .first()

    @staticmethod
    def find_by_teacher_id(teacher_id: int) -> 'List[StudentTeacherRequest]':
        return services.db.session.query(StudentTeacherRequest).filter_by(teacher_id=teacher_id).all()

    @staticmethod
    def find_by_student_id(student_id: int) -> 'List[StudentTeacherRequest]':
        return services.db.session.query(StudentTeacherRequest).filter_by(student_id=student_id).all()

    @staticmethod
    def delete_by_teacher_id_and_student_id(teacher_id: int, student_id: int) -> 'StudentTeacherRequest':
        return services.db.session.query(StudentTeacherRequest).filter_by(teacher_id=teacher_id, student_id=student_id)\
            .delete()
