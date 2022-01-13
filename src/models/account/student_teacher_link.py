from typing import List

from sqlalchemy import Column, INT, ForeignKey

from src.services import services
from src.utils.postgres_serializer_mixing import PostgresSerializerMixin


class StudentTeacherLink(services.db.Base, PostgresSerializerMixin):
    __tablename__ = 'student_teacher_link'
    __table_args__ = {'schema': 'account'}

    teacher_id = Column(INT, ForeignKey('account.account.id'), primary_key=True, nullable=False, index=True)
    student_id = Column(INT, ForeignKey('account.account.id'), primary_key=True, nullable=False, index=True)

    def save_to_db(self):
        services.db.session.add(self)
        services.db.session.commit()

    @staticmethod
    def find_by_teacher_id_and_student_id(teacher_id: int, student_id: int) -> 'StudentTeacherLink':
        return services.db.session.query(StudentTeacherLink).filter_by(teacher_id=teacher_id, student_id=student_id)\
            .first()

    @staticmethod
    def find_by_teacher_id(teacher_id: int) -> 'List[StudentTeacherLink]':
        return services.db.session.query(StudentTeacherLink).filter_by(teacher_id=teacher_id).all()

    @staticmethod
    def find_by_student_id(student_id: int) -> 'List[StudentTeacherLink]':
        return services.db.session.query(StudentTeacherLink).filter_by(student_id=student_id).all()

    @staticmethod
    def delete_by_teacher_id_and_student_id(teacher_id: int, student_id: int) -> 'StudentTeacherLink':
        return services.db.session.query(StudentTeacherLink).filter_by(teacher_id=teacher_id, student_id=student_id)\
            .delete()
