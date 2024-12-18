from cryptography.fernet import Fernet
import base64
import hashlib
from django.conf import settings
import secrets
import time

def generate_access_token():
    # Generate a random token
    token = secrets.token_urlsafe(32)
    # Add timestamp for expiration
    timestamp = str(int(time.time()))
    return f"{token}.{timestamp}"

def validate_token(token):
    try:
        token_parts = token.split('.')
        if len(token_parts) != 2:
            return False
        
        token_value, timestamp = token_parts
        # Check if token is expired (24 hours)
        if int(time.time()) - int(timestamp) > 86400:
            return False
        
        return True
    except:
        return False

def encrypt_payload(payload):
    key = settings.SECRET_KEY.encode()[:32].ljust(32, b'=')
    f = Fernet(base64.urlsafe_b64encode(key))
    return f.encrypt(payload.encode()).decode()

def decrypt_payload(encrypted_payload):
    key = settings.SECRET_KEY.encode()[:32].ljust(32, b'=')
    f = Fernet(base64.urlsafe_b64encode(key))
    return f.decrypt(encrypted_payload.encode()).decode()
