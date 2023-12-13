from typing import Any, Coroutine
from sqladmin import ModelView
from libs.auth_utils import get_password_hash

from models.user_models import User, Invitation


class UserAdmin(ModelView, model=User):
    name = "User"
    name_plural = "Users"
    icon = "fa fa-user"
    category = "User Management"

    column_list = [
        User.id,
        User.full_name,
        User.email,
        User.role,
        User.phone_number,
        User.profile_picture,
    ]

    column_searchable_list = [
        User.full_name,
        User.email,
        User.role,
        User.phone_number,
    ]

    column_details_exclude_list = [
        User.hr_profile,
        User.invitation,
    ]

    form_excluded_columns = [
        User.created_at,
        User.updated_at,
        User.hr_profile,
        User.invitation,
    ]


    def on_model_change(self, data: dict, model: Any, is_created: bool) -> Coroutine[Any, Any, None]:
        if "password" in data:
            data["password"] = get_password_hash(data["password"])
        return super().on_model_change(data, model, is_created)

class InvitationAdmin(ModelView, model=Invitation):
    name = "Invitation"
    name_plural = "Invitations"
    icon = "fa fa-mail-bulk"
    category = "User Management"

    column_list = [
        Invitation.id,
        Invitation.user,
        Invitation.receiver_email,
        Invitation.receiver_role,
        Invitation.invite_code,
        Invitation.has_used,
    ]

    column_searchable_list = [
        Invitation.receiver_role,
        Invitation.receiver_role,
        Invitation.invite_code,
        Invitation.has_used,
    ]