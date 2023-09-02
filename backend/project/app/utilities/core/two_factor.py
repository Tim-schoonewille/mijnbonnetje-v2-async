from pathlib import Path

from fastapi import BackgroundTasks

from app import models
from app.config import settings
from app.utilities.core.email import send_mail


def send_otp(
    to: str,
    otp_object: dict,
    bg_tasks: BackgroundTasks,
):
    send_otp_template_path = Path("./app/templates/send_otp.html")
    with open(send_otp_template_path, "r") as f:
        template = f.read()
    otp_model = models.TwoFactorSchema(**otp_object)
    link = (
        f"{settings.TWO_FACTOR_VERIFICATION_LINK}"
        f"?otp_session_id={otp_model.id}"
        f"&otp={otp_model.code}"
    )
    bg_tasks.add_task(
        func=send_mail,
        to=to,
        subject="Verify two-factor",
        html_template=template,
        render_kwargs={
            "session_id": otp_model.id,
            "code": otp_model.code,
            "link": link,
        },
    )

    return None
