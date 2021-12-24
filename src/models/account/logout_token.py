from datetime import datetime

from sqlalchemy import Column, INT, DateTime, String

from src.services import services
from src.utils.postgres_serializer_mixing import PostgresSerializerMixin


class LogoutToken(services.db.Base, PostgresSerializerMixin):
    __tablename__ = 'logout_token'
    __table_args__ = {'schema': 'account'}

    id = Column(INT, primary_key=True, unique=True, nullable=False)
    jti = Column(String(36), nullable=False, index=True)
    created_date = Column(DateTime, default=datetime.utcnow)

    def __init__(self, jti: str):
        self.jti = jti

    def save_to_db(self):
        services.db.session.add(self)
        services.db.session.commit()

    @staticmethod
    def find_by_jti(jti) -> 'LogoutToken':
        return services.db.session.query(LogoutToken).filter_by(jti=jti).first()

    @staticmethod
    def delete_by_id(id):
        return services.db.session.query(LogoutToken).filter_by(id=id).delete()
