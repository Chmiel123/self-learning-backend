from datetime import datetime
import enum

from sqlalchemy import Column, INT, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import TEXT, ENUM
from sqlalchemy.orm import relationship

from src.models.system.entity_status import EntityStatus
from src.services import services
from src.utils.postgres_serializer_mixing import PostgresSerializerMixin


class LessonGroup(services.db.Base, PostgresSerializerMixin):
    __tablename__ = 'lesson_group'
    __table_args__ = {'schema': 'system'}

    id = Column(INT, primary_key=True, unique=True, nullable=False)
    author_id = Column(INT, nullable=False, index=True)
    category_id = Column(INT, nullable=False)
    name = Column(TEXT, nullable=False, unique=True, index=True)
    content = Column(TEXT, nullable=False)
    status = Column(ENUM(EntityStatus), nullable=False, default=EntityStatus.draft)
    likes = Column(INT, default=0)
    dislikes = Column(INT, default=0)
    target_language_id = Column(INT, ForeignKey('system.language.id', ondelete='CASCADE'), nullable=False,
                                primary_key=True)
    created_date = Column(DateTime, default=datetime.utcnow)

    lessons = relationship('Lesson', backref='parent')
    target_language = relationship('Language')

    def __init__(self, author_id: int, name: str, content: str):
        self.author_id = author_id
        self.name = name
        self.content = content

    def save_to_db(self):
        services.db.session.add(self)
        services.db.session.commit()

    @staticmethod
    def find_by_id(id: int) -> 'LessonGroup':
        return services.db.session.query(LessonGroup).filter_by(id=id).first()

    @staticmethod
    def find_by_author_id(author_id) -> 'List[LessonGroup]':
        return services.db.session.query(LessonGroup).filter_by(author_id=author_id).all()

    @staticmethod
    def find_by_category_id(category_id) -> 'List[LessonGroup]':
        return services.db.session.query(LessonGroup).filter_by(category_id=category_id).all()

    @staticmethod
    def search_in_content(search_string) -> 'List[LessonGroup]':
        return services.db.session.query(LessonGroup).filter(LessonGroup.content.contains(search_string)).all()

    @staticmethod
    def delete_by_id(id):
        return services.db.session.query(LessonGroup).filter_by(id=id).delete()
