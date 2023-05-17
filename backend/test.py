from passlib.context import CryptContext
import os

os.system('clear')

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


plain_text = "kuba123"
hashed_pass1 = get_password_hash(plain_text)
hashed_pass2 = get_password_hash(plain_text)
hashed_pass3 = get_password_hash(plain_text)

plain_text = 'kuba123'

print(hashed_pass1)
print(hashed_pass2)
print(hashed_pass3)
print(verify_password(plain_text, hashed_pass3))