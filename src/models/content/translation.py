from sqlalchemy import Column, INT
from sqlalchemy.dialects.postgresql import ENUM

from src.models.system.entity_type import EntityType
from src.services import services
from src.utils.postgres_serializer_mixing import PostgresSerializerMixin


class Translation(services.db.Base, PostgresSerializerMixin):
    __tablename__ = 'translation'
    __table_args__ = {'schema': 'content'}

    source_id = Column(INT, primary_key=True, unique=False, nullable=False)
    target_id = Column(INT, primary_key=True, unique=False, nullable=False)
    entity_type = Column(ENUM(EntityType), primary_key=True, nullable=False)

    def save_to_db(self):
        services.db.session.add(self)
        services.db.session.commit()

    @staticmethod
    def find_by_source_id_and_target_id(source_id: int, target_id: int, entity_type: EntityType) -> 'List[Translation]':
        return services.db.session.query(Translation)\
            .filter_by(source_id=source_id, target_id=target_id, entity_type=entity_type).all()

    @staticmethod
    def find_by_source_id(source_id: int, entity_type: EntityType) -> 'List[Translation]':
        return services.db.session.query(Translation).filter_by(source_id=source_id, entity_type=entity_type).all()

    @staticmethod
    def find_by_target_id(target_id: int, entity_type: EntityType) -> 'List[Translation]':
        return services.db.session.query(Translation).filter_by(target_id=target_id, entity_type=entity_type).all()

    @staticmethod
    def delete_by_id(id):
        return services.db.session.query(Translation).filter_by(id=id).delete()
