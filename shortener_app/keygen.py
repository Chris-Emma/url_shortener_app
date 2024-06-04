import secrets
import string

def create_random_key(length: int = 5) -> str:
    """String module to generate ASCII characters
    - secrets module secretly choses five characters from chars"""
    chars = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(chars) for _ in range(length))