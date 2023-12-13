from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from models.basemodel import BaseMixin
from db import Base


class HrProfile(Base, BaseMixin):
    __tablename__ = "hr_profiles"

    id = Column(Integer, primary_key=True, index=True)
    hr_team = Column(String)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    user = relationship("User", back_populates="hr_profile")
