import secrets
from collections.abc import Set
from datetime import datetime, timedelta

from pydantic import EmailStr, PositiveInt
from redis.asyncio import Redis

def rand_6_digits() -> int:
    """Returns a 6 digit integer.
    
    Range is between `100,000` and `999,999` inclusive.
    """
    _sysrand = secrets.SystemRandom(None)
    return _sysrand.randrange(100_000, 1_000_000)



async def gen_otp_password(*, redis_client: Redis, email: EmailStr, min_to_exp = 1) -> int:
    """Generate a one time password with an expiration date.
    
    `otp` is stored in Redis as a value for `email`, the key. 
    After `min_to_exp` min(s), the OTP is expired.
    """
    otp = rand_6_digits()
    expires = datetime.now() + timedelta(seconds=60 * min_to_exp)
    await _add_otp_to_redis(redis_client=redis_client,
                            otp=otp, 
                            email=email,
                            expire=expires)
    return otp


async def _add_otp_to_redis(*, redis_client: Redis, otp: PositiveInt, email: EmailStr, expire: datetime):
    await redis_client.set(email, str(otp))
    await redis_client.expireat(email, when=expire)


async def check_otp_for_email(*, redis_client: Redis, otp: PositiveInt, email: EmailStr) -> bool:
    """Verifies that the OTP provided exists for the email provided.
    
    Returns false if the OTP is expired, doesn't exist, or if the email is wrong (even if the OTP is right).

    """
    resp: str | None = await redis_client.get(email)
    if resp and resp == str(otp) :
        return True
    return False
