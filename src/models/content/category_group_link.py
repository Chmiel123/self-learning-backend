from sqlalchemy import Column, INT, ForeignKey

from src.services import services
from src.utils.postgres_serializer_mixing import PostgresSerializerMixin


class CategoryGroupLink(services.db.Base, PostgresSerializerMixin):
    __tablename__ = 'category_group_link'
    __table_args__ = {'schema': 'content'}

    top_id = Column(INT, ForeignKey('content.category.id'), primary_key=True)
    bottom_id = Column(INT, ForeignKey('content.lesson_group.id'), primary_key=True)

    def __init__(self, top_id: int, bottom_id: int):
        self.top_id = top_id
        self.bottom_id = bottom_id

    def save_to_db(self):
        services.db.session.add(self)
        services.db.session.commit()

    @staticmethod
    def find_by_top_id_bottom_id(top_id: int, bottom_id: int):
        return services.db.session.query(CategoryGroupLink).filter_by(top_id=top_id, bottom_id=bottom_id).first()

    @staticmethod
    def find_by_top_id(top_id: int) -> 'List[CategoryGroupLink]':
        return services.db.session.query(CategoryGroupLink).filter_by(top_id=top_id).all()

    @staticmethod
    def find_by_bottom_id(bottom_id: int) -> 'List[CategoryGroupLink]':
        return services.db.session.query(CategoryGroupLink).filter_by(bottom_id=bottom_id).all()

    @staticmethod
    def delete_by_top_id_bottom_id(top_id: int, bottom_id: int):
        return services.db.session.query(CategoryGroupLink).filter_by(top_id=top_id, bottom_id=bottom_id).delete()
