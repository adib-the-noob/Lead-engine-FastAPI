import os
import smtplib
from dotenv import load_dotenv
from email.message import EmailMessage

from models import user_models

load_dotenv()

password = os.getenv("GMAIL_APP_PASSWORD")
sender_email = os.getenv("GMAIL_APP_EMAIL")


def send_email(
    receiver_email: str,
    receiver_role: user_models.UserRoles,
    invite_code: str,
):  
    em = EmailMessage()
    em[
        "Subject"
    ] = f"You have been invited to join the team as a {receiver_role.value}"
    em["From"] = sender_email
    em["To"] = receiver_email
    body = f"""
    Hi, you have been invited to join the team as a {receiver_role.value}. Please click the link below to register.
    http://localhost:8000/auth/register?invite_code={invite_code}
    """
    em.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender_email, password=password)
        smtp.sendmail(sender_email, receiver_email, em.as_string())
