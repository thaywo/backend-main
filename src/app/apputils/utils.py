import base64
import hashlib
import random
import string
from datetime import datetime, timezone

def generate_referral_code():
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(6))