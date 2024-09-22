import logging
from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from pydantic import EmailStr, BaseModel, PositiveInt

from auth_prac.utils import gen_otp_password, check_otp_for_email
from auth_prac.deps import RedisDep

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(f"     {__name__}")


app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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


@app.post("/token")
async def login_route(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], redis: RedisDep):
    """Actual route where API will try and authenticate user.
    
    This is the relative API route that OAuth2PasswordBearer points to whenever it resolves Depends.
    """
    # Usually check if the User exists in the database
    user_dict = {"Something": "so it isn't null"} # method to get current user, or None if doesn't exist
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    # Verify that Email has password attached
    email_pass_match = await check_otp_for_email(redis_client=redis,
                                       otp=form_data.password,
                                       email=form_data.username)
    if not email_pass_match:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    # MUST return object with the fields as shown below:
    # https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/#return-the-token
    return {"access_token": form_data.username, "token_type": "bearer"}


@app.get("/fake_protected_endpoint")
async def fake_protected_endpoint(token: Annotated[str, Depends(oauth2_scheme)]):
    """API endpoint that only works when user is authenticated.
    
    Displays token and message if the user is logged in correctly.
    """

    return {"message": "You're logged in!",
            "token": token}
