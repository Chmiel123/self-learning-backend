from datetime import datetime
from typing import List

from sqlalchemy import Column, INT, DateTime, ForeignKey, SMALLINT
from sqlalchemy.dialects.postgresql import TEXT, ENUM

from src.models.system.entity_status import EntityStatus
from src.models.system.lesson_type import LessonType
from src.services import services
from src.utils.postgres_serializer_mixing import PostgresSerializerMixin


class Lesson(services.db.Base, PostgresSerializerMixin):
    __tablename__ = 'lesson'
    __table_args__ = {'schema': 'content'}

    id = Column(INT, primary_key=True, unique=True, nullable=False, index=True)
    course_id = Column(INT, ForeignKey('content.course.id'), nullable=False, index=True)
    author_id = Column(INT, nullable=False, index=True)
    type = Column(ENUM(LessonType), nullable=False, default=LessonType.lesson)
    duration_minutes = Column(SMALLINT, nullable=True)
    order = Column(SMALLINT)
    name = Column(TEXT, nullable=False)
    content = Column(TEXT, nullable=False)
    status = Column(ENUM(EntityStatus), nullable=False, default=EntityStatus.draft)
    likes = Column(INT, default=0)
    dislikes = Column(INT, default=0)
    language_id = Column(SMALLINT, ForeignKey('system.language.id'), nullable=False)
    created_date = Column(DateTime, default=datetime.utcnow)

    def save_to_db(self):
        services.db.session.add(self)
        services.db.session.commit()

    @staticmethod
    def find_by_id(id: int) -> 'Lesson':
        return services.db.session.query(Lesson).filter_by(id=id).first()

    @staticmethod
    def find_by_course_id(course_id: int) -> 'List[Lesson]':
        return services.db.session.query(Lesson).filter_by(course_id=course_id).all()

    @staticmethod
    def find_by_author_id(author_id: int) -> 'List[Lesson]':
        return services.db.session.query(Lesson).filter_by(author_id=author_id).all()

    @staticmethod
    def search_in_content(search_string: str) -> 'List[Lesson]':
        return services.db.session.query(Lesson).filter(Lesson.content.contains(search_string)).all()

    @staticmethod
    def delete_by_id(id):
        return services.db.session.query(Lesson).filter_by(id=id).delete()
