from passlib.context import CryptContext

pswd_ctx = CryptContext(
    schemes=['bcrypt'],
    deprecated='auto'
)

def hash_pswd(pswd: str):
    return pswd_ctx.hash(pswd.strip()[:72])

def verify_pswd(plain_pswd: str, hash_pswd: str):
    return pswd_ctx.verify(plain_pswd, hash_pswd)