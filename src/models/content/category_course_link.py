from typing import List

from sqlalchemy import Column, INT, ForeignKey

from src.services import services
from src.utils.postgres_serializer_mixing import PostgresSerializerMixin


class CategoryCourseLink(services.db.Base, PostgresSerializerMixin):
    __tablename__ = 'category_course_link'
    __table_args__ = {'schema': 'content'}

    category_id = Column(INT, ForeignKey('content.category.id'), primary_key=True)
    course_id = Column(INT, ForeignKey('content.course.id'), primary_key=True)

    def save_to_db(self):
        services.db.session.add(self)
        services.db.session.commit()

    @staticmethod
    def find_by_category_id_course_id(category_id: int, course_id: int):
        return services.db.session.query(CategoryCourseLink)\
            .filter_by(category_id=category_id, course_id=course_id).first()

    @staticmethod
    def find_by_category_id(category_id: int) -> 'List[CategoryCourseLink]':
        return services.db.session.query(CategoryCourseLink).filter_by(category_id=category_id).all()

    @staticmethod
    def find_by_course_id(course_id: int) -> 'List[CategoryCourseLink]':
        return services.db.session.query(CategoryCourseLink).filter_by(course_id=course_id).all()

    @staticmethod
    def delete_by_category_id_course_id(category_id: int, course_id: int):
        return services.db.session.query(CategoryCourseLink)\
            .filter_by(category_id=category_id, course_id=course_id).delete()
