from app.config import settings
from app.utils import *


def main():
    print("Hello World")
    print(settings.model_dump())
    create_and_send_basic(email_to=settings.EMAIL_TO_ADDR)


def create_and_send_basic(*, email_to):
    """Create and send a basic email."""
    data: EmailData = generate_basic_email()
    send_email(email_to=email_to, 
               subject=data.subject,
               html_content=data.html_content
    )


if __name__=="__main__":
    main()
