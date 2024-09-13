import secrets


def rand_6_digits() -> int:
    """Returns a 6 digit integer.
    
    Range is between `100,000` and `999,999` inclusive.
    """
    _sysrand = secrets.SystemRandom(None)
    return _sysrand.randrange(100_000, 1_000_000)



def gen_otp_password() -> int:
    """Generate a one time password with an expiration date.
    
    Right now, exists so more things can go in gen_otp_password late.
    """
    otp = rand_6_digits()
    return otp
