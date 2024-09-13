import logging
from fastapi import FastAPI

from pydantic import EmailStr, BaseModel

from auth_prac.utils import gen_otp_password

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(f"     {__name__}")


app = FastAPI()

list_of_otps = {}


@app.get("/")
async def app_root():
    return {"message": "At App Root."}


class Email(BaseModel):
    email: EmailStr

@app.post("/fake_send_otp_to_email")
async def fake_send_otp_to_email(email: Email):
    """Log a OTP to the apps logger."""
    otp_pass = gen_otp_password()
    logger.info(f" OTP for {email.email} is {otp_pass}")
    return {f"Email sent to {email.email} containing OTP."}