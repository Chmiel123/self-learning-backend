import uuid
import bcrypt
from sqlalchemy import Column, ForeignKey, INT
from sqlalchemy.dialects.postgresql import UUID, TEXT

from src.services import services
from src.services.postgres_serializer_mixing import PostgresSerializerMixin
from src.services.services import db, flask


class Account(services.db.Base, PostgresSerializerMixin):
    __tablename__ = 'account'
    __table_args__ = {'schema': 'account'}

    id = Column(INT, primary_key=True, unique=True, nullable=False)
    password = Column(TEXT, nullable=False)

    def __init__(self, id: int, password: str):
        self.id = id
        self.password = Account.generate_hash(password)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def generate_hash(password):
        salt = bcrypt.gensalt(rounds=flask.config['BCRYPT_ROUNDS'])
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    @staticmethod
    def verify_hash(password, hashed):
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

    @staticmethod
    def delete_by_id(id):
        return db.session.query(Account).filter_by(id=id).delete()
