from enum import Enum as PyEnum

from sqlalchemy import Column, String, Integer, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship

from models.basemodel import BaseMixin
from db import Base

# for invite_code generation
import secrets
import string
from datetime import datetime, timedelta


class UserRoles(PyEnum):
    bizdev = "bizdev"
    admin = "admin"
    cs = "cs"
    hr = "hr"
    content_dev = "content_dev"


class User(Base, BaseMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    email = Column(String, unique=True)
    role = Column(Enum(UserRoles), default=UserRoles.cs)
    phone_number = Column(String, unique=True)
    profile_picture = Column(String)
    password = Column(String)

    hr_profile = relationship("HrProfile", uselist=False, back_populates="user")
    invitation = relationship("Invitation", back_populates="user")

    def __str__(self):
        return f"{self.full_name}"
    
    def profile_picture_url(self):
        return f"http://127.0.0.1:8000/{self.profile_picture}"


class Invitation(Base, BaseMixin):  
    __tablename__ = "invitations"

    id = Column(Integer, primary_key=True, index=True)
    invite_code = Column(String, unique=True)
    receiver_email = Column(String, unique=True)
    receiver_role = Column(Enum(UserRoles))
    has_used = Column(String, default=False)
    expiration_date = Column(DateTime, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    user = relationship("User", back_populates="invitation")

    def __str__(self):
        return f"{self.receiver_email} - {self.receiver_role}"

    def save(self, db):
        characters = string.ascii_letters + string.digits
        code = "".join(secrets.choice(characters) for _ in range(32))
        self.invite_code = code
        self.expiration_date = datetime.now() + timedelta(days=1)
        super().save(db)
