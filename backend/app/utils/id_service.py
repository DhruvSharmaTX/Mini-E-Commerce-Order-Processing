from sqlalchemy.orm import Session
from sqlalchemy import func


def unique_id(db: Session, model, prefix: str):

    last_record = db.query(func.max(model.id)).scalar()

    if not last_record:
        return f"{prefix}001"

    last_number = int(last_record.replace(prefix, ""))

    new_number = last_number + 1

    return f"{prefix}{new_number:03d}"