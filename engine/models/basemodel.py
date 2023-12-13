from datetime import datetime
from sqlalchemy import Column, DateTime


class BaseMixin:
    __abstract__ = True
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def save(self, db):
        db.add(self)
        db.commit()
        db.refresh(self)
        return self
