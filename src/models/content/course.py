from datetime import datetime

from sqlalchemy import Column, INT, DateTime, ForeignKey, SMALLINT
from sqlalchemy.dialects.postgresql import TEXT, ENUM
from sqlalchemy.orm import relationship

from src.models.content.category import Category
from src.models.content.category_course_link import CategoryCourseLink
from src.models.system.entity_status import EntityStatus
from src.services import services
from src.utils.postgres_serializer_mixing import PostgresSerializerMixin


class Course(services.db.Base, PostgresSerializerMixin):
    __tablename__ = 'course'
    __table_args__ = {'schema': 'content'}

    id = Column(INT, primary_key=True, unique=True, nullable=False, index=True)
    author_id = Column(INT, nullable=False, index=True)
    name = Column(TEXT, nullable=False, index=True)
    content = Column(TEXT, nullable=False)
    status = Column(ENUM(EntityStatus), nullable=False, default=EntityStatus.draft)
    likes = Column(INT, default=0)
    dislikes = Column(INT, default=0)
    language_id = Column(SMALLINT, ForeignKey('system.language.id', ondelete='CASCADE'), nullable=False)
    created_date = Column(DateTime, default=datetime.utcnow)

    def save_to_db(self):
        services.db.session.add(self)
        services.db.session.commit()

    def get_parents(self):
        return services.db.session.query(Category)\
            .join(CategoryCourseLink, Category.id == CategoryCourseLink.category_id).filter_by(course_id=self.id).all()

    @staticmethod
    def find_by_id(id: int) -> 'Course':
        return services.db.session.query(Course).filter_by(id=id).first()

    @staticmethod
    def find_by_author_id(author_id) -> 'List[Course]':
        return services.db.session.query(Course).filter_by(author_id=author_id).all()

    @staticmethod
    def find_by_category_id(category_id: int, page_number: int, page_size: int) -> 'List[Course]':
        return services.db.session.query(Course)\
            .join(CategoryCourseLink, Course.id == CategoryCourseLink.course_id)\
            .filter_by(category_id=category_id).order_by(Course.likes).limit(page_size)\
            .offset((page_number - 1) * page_size).all()

    @staticmethod
    def search_in_content(search_string) -> 'List[Course]':
        return services.db.session.query(Course).filter(Course.content.contains(search_string)).all()

    @staticmethod
    def delete_by_id(id):
        return services.db.session.query(Course).filter_by(id=id).delete()
