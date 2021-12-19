from datetime import datetime

from sqlalchemy import Column, INT, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.orm import relationship

from src.services import services
from src.utils.postgres_serializer_mixing import PostgresSerializerMixin


class Lesson(services.db.Base, PostgresSerializerMixin):
    __tablename__ = 'lesson'
    __table_args__ = {'schema': 'system'}

    id = Column(INT, primary_key=True, unique=True, nullable=False)
    group_id = Column(INT, ForeignKey('system.lesson_group.id', ondelete='CASCADE'), nullable=False, index=True)
    author_id = Column(INT, nullable=True, index=True)
    name = Column(TEXT, nullable=False, unique=True)
    content = Column(TEXT, nullable=False)
    likes = Column(INT, default=0)
    dislikes = Column(INT, default=0)
    target_language_id = Column(INT, ForeignKey('system.language.id', ondelete='CASCADE'), nullable=False,
                                primary_key=True)
    created_date = Column(DateTime, default=datetime.utcnow)

    target_language = relationship("Language")

    def __init__(self, author_id: int, name: str, content: str):
        self.author_id = author_id
        self.name = name
        self.content = content

    def save_to_db(self):
        services.db.session.add(self)
        services.db.session.commit()

    @staticmethod
    def find_by_id(id: int) -> 'Lesson':
        return services.db.session.query(Lesson).filter_by(id=id).first()

    @staticmethod
    def find_by_parent_id(parent_id) -> 'Lesson':
        return services.db.session.query(Lesson).filter_by(parent_id=parent_id).all()

    @staticmethod
    def find_by_author_id(author_id) -> 'Lesson':
        return services.db.session.query(Lesson).filter_by(author_id=author_id).all()

    @staticmethod
    def search_in_content(search_string) -> 'Lesson':
        return services.db.session.query(Lesson).filter(Lesson.content.contains(search_string)).all()

    @staticmethod
    def delete_by_id(id):
        return services.db.session.query(Lesson).filter_by(id=id).delete()
