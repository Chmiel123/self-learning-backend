import uuid

from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy_serializer import SerializerMixin


class PostgresSerializerMixin(SerializerMixin):
    serialize_types = (
        (uuid.UUID, str),
        (TEXT, str)
    )
