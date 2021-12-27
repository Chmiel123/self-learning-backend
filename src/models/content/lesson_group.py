from datetime import datetime

from sqlalchemy import Column, INT, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import TEXT, ENUM
from sqlalchemy.orm import relationship

from src.models.content.category_group_link import CategoryGroupLink
from src.models.system.entity_status import EntityStatus
from src.services import services
from src.utils.postgres_serializer_mixing import PostgresSerializerMixin


class LessonGroup(services.db.Base, PostgresSerializerMixin):
    __tablename__ = 'lesson_group'
    __table_args__ = {'schema': 'content'}

    id = Column(INT, primary_key=True, unique=True, nullable=False)
    author_id = Column(INT, nullable=False, index=True)
    name = Column(TEXT, nullable=False, unique=True, index=True)
    content = Column(TEXT, nullable=False)
    status = Column(ENUM(EntityStatus), nullable=False, default=EntityStatus.draft)
    likes = Column(INT, default=0)
    dislikes = Column(INT, default=0)
    language_id = Column(INT, ForeignKey('system.language.id', ondelete='CASCADE'), nullable=False)
    created_date = Column(DateTime, default=datetime.utcnow)

    def __init__(self, author_id: int, name: str, content: str, language_id: int):
        self.author_id = author_id
        self.name = name
        self.content = content
        self.language_id = language_id

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
    def find_by_category_id(category_id: int, page_number: int, page_size: int) -> 'List[LessonGroup]':
        return services.db.session.query(LessonGroup)\
            .join(CategoryGroupLink, LessonGroup.id == CategoryGroupLink.group_id)\
            .filter_by(category_id=category_id).limit(page_size).offset((page_number - 1) * page_size).all()

    @staticmethod
    def search_in_content(search_string) -> 'List[LessonGroup]':
        return services.db.session.query(LessonGroup).filter(LessonGroup.content.contains(search_string)).all()

    @staticmethod
    def delete_by_id(id):
        return services.db.session.query(LessonGroup).filter_by(id=id).delete()
