"""Utility functions to assist in email sending."""
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from jinja2 import Template
from app.config import settings
import emails


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class EmailData:
    html_content: str
    subject: str



def render_email_template(*, template_name: str, context: dict[str, Any]) -> str:
    template_str = (
        Path(__file__).parent / "email_templates" / template_name
    ).read_text()
    html_content = Template(template_str).render(context)
    return html_content


def send_email(
        *,
        email_to: str,
        subject: str = "",
        html_content: str = "",
) -> None:
    assert settings.emails_enabled, "no provided configuration for email variables"

    message = emails.Message(
        subject=subject,
        html=html_content,
        mail_from=("No_Name_from", settings.EMAIL_FROM_ADDR),
        headers={"X-PM-Message-Stream": "outbound"} # required because I used PostMark
    )
    smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
    if settings.SMTP_TLS:
        smtp_options["tls"] = True
    elif settings.SMTP_SSL:
        smtp_options["ssl"] = True
    if settings.SMTP_USER:
        smtp_options["user"] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        smtp_options["password"] = settings.SMTP_PASSWORD

    response = message.send(to=email_to, smtp=smtp_options)
    logger.info(f"Sent Email result: {response}")


def generate_basic_email() -> EmailData:
    subject = "Basic Email"
    html_content = render_email_template(
        template_name="basic.html",
        context={}
    )
    return EmailData(html_content=html_content, subject=subject)
