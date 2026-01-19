from passlib.context import CryptContext
import re

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
specials = re.compile(r'[@_!#$%^&*()<>?/\|}{~:]')
numbers = re.compile('[0-9]')


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def check_password_complexity(password):
    return len(password) >= 8 \
        and any(ele.isupper() for ele in password) \
        and any(ele.islower() for ele in password) \
        and numbers.search(password) \
        and specials.search(password)
