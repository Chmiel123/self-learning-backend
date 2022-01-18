import enum


class EntityStatus(enum.Enum):
    draft = 1
    active = 2
    deleted = 3
    draft_invalid = 4
