from sqlalchemy import Column, INT, String
from sqlalchemy.dialects.postgresql import TEXT

from src.services import services
from src.utils.error_code import ErrorCode
from src.utils.exceptions import ErrorException, LanguageCodeNotFoundException
from src.utils.postgres_serializer_mixing import PostgresSerializerMixin


class Language(services.db.Base, PostgresSerializerMixin):
    __tablename__ = 'language'
    __table_args__ = {'schema': 'system'}

    id = Column(INT, primary_key=True, unique=False, nullable=False)
    # ISO 639-1 Code
    code = Column(String(5), nullable=False)
    english_name = Column(TEXT)
    native_name = Column(TEXT)

    def __init__(self, code: str, english_name: str, native_name: str):
        self.code = code
        self.english_name = english_name
        self.native_name = native_name

    def save_to_db(self):
        services.db.session.add(self)
        services.db.session.commit()

    def serialize(self):
        return {
            'id': self.id,
            'code': self.code,
            'english_name': self.english_name,
            'native_name': self.native_name
        }

    @staticmethod
    def find_all() -> 'List[Language]':
        return services.db.session.query(Language).all()

    @staticmethod
    def find_by_code(code: code) -> 'Language':
        language = services.db.session.query(Language).filter_by(code=code).first()
        if not language:
            raise LanguageCodeNotFoundException([code])
        return language

    @staticmethod
    def find_by_id(id: int) -> 'Language':
        return services.db.session.query(Language).filter_by(id=id).first()
