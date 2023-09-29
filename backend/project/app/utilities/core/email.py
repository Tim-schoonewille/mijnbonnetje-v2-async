from typing import Any
from pathlib import Path

import emails  # type: ignore
from emails.template import JinjaTemplate as T  # type: ignore
from fastapi import BackgroundTasks

from app.config import get_settings


settings = get_settings()


def send_mail(
    to: str,
    subject: str,
    html_template: str,
    render_kwargs: dict[str, Any],
):
    message = emails.html(
        subject=subject,
        html=T(html_template),
        mail_from=(settings.MAIL_FROM_NAME, settings.MAIL_FROM_EMAIL),
    )
    response = message.send(
        to=(to, to),
        render=render_kwargs,
        smtp={
            "host": settings.SMTP_HOST,
            "port": settings.SMTP_PORT,
            "user": settings.SMTP_USER,
            "password": settings.SMTP_PASS,
        },
    )
    return response


def send_verification_code_email(
    to: str,
    code: str,
    bg_tasks: BackgroundTasks,
):
    email_template_path = Path("./app/templates/email_verification.html")
    with open(email_template_path, "r") as f:
        template = f.read()

    link = f"{settings.APP_FQDN}{settings.URL_PREFIX}auth/verify-email/?token={code}"
    subject = "Verify email address"
    # response = send_mail(
    #     to=to,
    #     subject=subject,
    #     html_template=template,
    #     render_kwargs={'link': link}
    # )

    bg_tasks.add_task(
        func=send_mail,
        to=to,
        subject=subject,
        html_template=template,
        render_kwargs={"link": link},
    )
    return None


def send_request_new_password_email(
    to: str,
    code: str,
    bg_tasks: BackgroundTasks,
):
    email_template_path = Path("./app/templates/new_password_request.html")
    with open(email_template_path, "r") as f:
        template = f.read()
    
    link = f'{settings.APP_FQDN}auth/verify-new-password?token={code}'
    subject = 'MIJNBONNETJE.nL :: New password request'
    bg_tasks.add_task(
        func=send_mail,
        to=to,
        subject=subject,
        html_template=template,
        render_kwargs={'link': link}
    )
    return None