from config import Config
from providers.email_provider import send_email


def send_welcome_email(to_email: str, user_name: str):
    subject = "Welcome to Our Platform"
    context = {
        "user_name": user_name
    }
    return send_email(
        to_email=to_email,
        subject=subject,
        template_name="welcome_template.html",
        context=context
    )

def send_forgot_password_email(to_email: str, reset_token: str):
    subject = "Password Reset Request"
    context = {
        "reset_link": f"{Config.FRONTEND_URL}/{reset_token}",
    }
    return send_email(
        to_email=to_email,
        subject=subject,
        template_name="forgot_password_template.html",
        context=context
    )

async def send_update_password_email(to_email: str, user_name: str):
    subject = "Password Updated Successfully"
    context = {
        "user_name": user_name
    }
    return await send_email(
        to_email=to_email,
        subject=subject,
        template_name="password_update_template.html",
        context=context
    )
