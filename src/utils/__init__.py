def modify(entity, value, field, changed):
    if getattr(entity, field) != value:
        setattr(entity, field, value)
        return True
    return changed
