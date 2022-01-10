from typing import Type

from src.utils.exceptions import IdRangeInvalidException, InvalidInputDataException


def modify(entity, value, field, changed):
    if getattr(entity, field) != value:
        setattr(entity, field, value)
        return True
    return changed


def parse_id_range(id_range: str):
    split = id_range.split('-')
    try:
        return int(split[0]), int(split[1])
    except (ValueError, IndexError):
        raise IdRangeInvalidException([id_range])


def assert_type(value, ttype: Type):
    if not isinstance(value, ttype):
        raise InvalidInputDataException([str(value), ttype.__name__])


def assert_type_nullable(value, ttype: Type):
    if value is not None and not isinstance(value, ttype):
        raise InvalidInputDataException([str(value), ttype.__name__])
