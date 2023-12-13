from pydantic import BaseModel, EmailStr
from fastapi import UploadFile, File, Form
from models.user_models import UserRoles


class UserRegister(BaseModel):
    full_name: str = Form(max_length=50)
    phone_number: str = Form(max_length=15)
    profile_picture: UploadFile = File(None)
    password: str = Form(max_length=50)

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str   
    token_type: str

class InvitationEmail(BaseModel):
    receiver_role : UserRoles
    receiver_email: EmailStr
