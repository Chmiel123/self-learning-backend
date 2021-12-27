from typing import List

from sqlalchemy import Column, INT, ForeignKey

from src.services import services
from src.utils.postgres_serializer_mixing import PostgresSerializerMixin


class CategoryGroupLink(services.db.Base, PostgresSerializerMixin):
    __tablename__ = 'category_group_link'
    __table_args__ = {'schema': 'content'}

    category_id = Column(INT, ForeignKey('content.category.id'), primary_key=True)
    group_id = Column(INT, ForeignKey('content.lesson_group.id'), primary_key=True)

    def __init__(self, category_id: int, group_id: int):
        self.category_id = category_id
        self.group_id = group_id

    def save_to_db(self):
        services.db.session.add(self)
        services.db.session.commit()

    @staticmethod
    def find_by_top_id_bottom_id(category_id: int, group_id: int):
        return services.db.session.query(CategoryGroupLink)\
            .filter_by(category_id=category_id, group_id=group_id).first()

    @staticmethod
    def find_by_category_id(category_id: int) -> 'List[CategoryGroupLink]':
        return services.db.session.query(CategoryGroupLink).filter_by(category_id=category_id).all()

    @staticmethod
    def find_by_group_id(group_id: int) -> 'List[CategoryGroupLink]':
        return services.db.session.query(CategoryGroupLink).filter_by(group_id=group_id).all()

    @staticmethod
    def delete_by_category_id_group_id(category_id: int, group_id: int):
        return services.db.session.query(CategoryGroupLink)\
            .filter_by(category_id=category_id, group_id=group_id).delete()
