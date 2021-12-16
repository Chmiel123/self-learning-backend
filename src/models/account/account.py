import datetime
import bcrypt
from sqlalchemy import Column, ForeignKey, INT, DateTime
from sqlalchemy.dialects.postgresql import UUID, TEXT

from src.services import services
from src.services.postgres_serializer_mixing import PostgresSerializerMixin


class Account(services.db.Base, PostgresSerializerMixin):
    __tablename__ = 'account'
    __table_args__ = {'schema': 'account'}

    id = Column(INT, primary_key=True, unique=True, nullable=False)
    name = Column(TEXT, nullable=False, unique=True, index=True)
    email = Column(TEXT, nullable=True, unique=True, index=True)
    password = Column(TEXT, nullable=False)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, name: str, password: str):
        self.name = name
        self.email = None
        self.password = Account.generate_hash(password)

    def save_to_db(self):
        services.db.session.add(self)
        services.db.session.commit()

    def is_email_verified(self):
        return self.email is not None

    @staticmethod
    def generate_hash(password):
        salt = bcrypt.gensalt(rounds=services.flask.config['BCRYPT_ROUNDS'])
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    @staticmethod
    def verify_hash(password, hashed):
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

    @staticmethod
    def find_by_id(id: int) -> 'Account':
        return services.db.session.query(Account).filter_by(id=id).first()

    @staticmethod
    def find_by_username(username) -> 'Account':
        return services.db.session.query(Account).filter_by(name=username).first()

    @staticmethod
    def find_by_email(email) -> 'Account':
        return services.db.session.query(Account).filter_by(email=email).first()

    @staticmethod
    def delete_by_id(id):
        return services.db.session.query(Account).filter_by(id=id).delete()
