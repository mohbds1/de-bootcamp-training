from passlib.context import CryptContext

# استخدم pbkdf2_sha256 بدل bcrypt لتفادي مشاكل التوافق وحد 72 بايت
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# alias للاسم المستخدم في السكربت seed.py
def get_password_hash(password: str) -> str:
    return hash_password(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)