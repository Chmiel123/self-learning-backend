from src.utils.exceptions import IdRangeInvalidException


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
