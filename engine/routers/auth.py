from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.background import BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm

from models import user_models

from db import db_dependency
from schemas import auth
from libs.auth_utils import (
    create_access_token,
    authenticate_user,
    create_user,
    user_dependency,
    save_image
)
from libs.email_sender import send_email

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


@router.post("/token", response_model=auth.Token)
def loging_for_access_token(
    db: db_dependency,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        return JSONResponse(
            status_code=401,
            content={"message": "Incorrect email or password"},
        )

    token = create_access_token(
        data={
            "sub": user.email,
            "user_id": user.id,
            "role": user.role.value,
        },
    )
    return JSONResponse(
        status_code=200,
        content={
            "access_token": token,
            "token_type": "bearer",
        },
    )


@router.post("/register", response_model=None)
async def user_registration(
    invite_code: str,
    db: db_dependency,
    user: auth.UserRegister = Depends(),
):
    invite_exists = (
        db.query(user_models.Invitation)
        .filter(user_models.Invitation.invite_code == invite_code)
        .first()
    )

    if invite_exists is None or invite_exists.has_used is True:
        return JSONResponse(
            status_code=400,
            content={
                "message": "Invalid invite code",
            },
        )

    user_obj = create_user(
        db,
        full_name=user.full_name,
        phone_number=user.phone_number,
        password=user.password,
        email=invite_exists.receiver_email,
        role=invite_exists.receiver_role,
        profile_picture=save_image(
            image=user.profile_picture,
            save_to_folder="media/profile_pictures",
        )
    )
    invite_exists.has_used = True
    invite_exists.save(db)

    return JSONResponse(
        status_code=200,
        content={
            "message": "User created successfully",
        },
    )


@router.post("/send-invitation-email", response_model=None)
def send_invitation_email(
    user: user_dependency,
    db: db_dependency,
    invitation: auth.InvitationEmail,
    background_tasks: BackgroundTasks,
):
    # check user role
    if user.role.value != "admin" and user.role.value != "hr":
        return JSONResponse(
            status_code=401,
            content={
                "message": "You don't have permission to send invitation email",
            },
        )

    # check if the email is already registered
    email_exists = (
        db.query(user_models.User)
        .filter(user_models.User.email == invitation.receiver_email)
        .first()
    )

    if email_exists is not None:
        return JSONResponse(
            status_code=400,
            content={
                "message": "Email already registered",
            },
        )

    # check if the email is already invited
    email_invited = (
        db.query(user_models.Invitation)
        .filter(user_models.Invitation.receiver_email == invitation.receiver_email)
        .first()
    )

    if email_invited is not None:
        return JSONResponse(
            status_code=400,
            content={
                "message": "Email already invited",
            },
        )

    # create invitation
    invite = user_models.Invitation(
        user_id=user.id,
        receiver_email=invitation.receiver_email,
        receiver_role=invitation.receiver_role.value,
    )
    invite.save(db)

    # send email
    background_tasks.add_task(
        send_email,
        invitation.receiver_email,
        invitation.receiver_role,
        invite.invite_code,
    )
    return JSONResponse(
        status_code=200,
        content={
            "message": "Invitation sent successfully",
        },
    )


