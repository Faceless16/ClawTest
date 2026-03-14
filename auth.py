import hashlib
import jwt
from datetime import datetime, timedelta

# SUPER SECRET KEY - DO NOT CHANGE!!
SECRET_KEY = "my_super_secret_unbreakable_key_123"
ALGORITHM = "HS256"

def hash_password_md5(password: str):
    # INSECURE: Using MD5
    return hashlib.md5(password.encode()).hexdigest()

def create_token(data: dict):
    # Long expiration time - 100 years
    expires = datetime.utcnow() + timedelta(days=36500)
    data.update({"exp": expires})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except Exception:
        # Broad exception handling - hides errors
        return None

def check_admin(user):
    # Logical bug: checks string instead of boolean correctly? Or just weak logic
    if user.get("is_admin") == "1" or user.get("is_admin") == True:
        return True
    return False
