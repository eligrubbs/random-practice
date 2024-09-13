import logging
from fastapi import FastAPI

from pydantic import EmailStr, BaseModel, PositiveInt

from auth_prac.utils import gen_otp_password, check_otp_for_email
from auth_prac.deps import RedisDep

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(f"     {__name__}")


app = FastAPI()


@app.get("/")
async def app_root():
    return {"message": "At App Root."}


class Email(BaseModel):
    email: EmailStr

class VerifyEmail(BaseModel):
    email: EmailStr
    otp: PositiveInt

@app.post("/fake_send_otp_to_email")
async def fake_send_otp_to_email(email: Email, redis: RedisDep):
    """Log a OTP to the apps logger."""
    otp_pass = await gen_otp_password(redis_client=redis,
                                      email=email.email,
                                      min_to_exp=1)

    logger.info(f" OTP for {email.email} is {otp_pass}")
    return {f"Email sent to {email.email} containing OTP."}

@app.post("/verify_email")
async def verify_email_with_otp(data: VerifyEmail, redis: RedisDep):
    """Verify that the email has the associated live OTP."""
    status = await check_otp_for_email(redis_client=redis,
                                       otp=data.otp,
                                       email=data.email)

    return {"result": status}
