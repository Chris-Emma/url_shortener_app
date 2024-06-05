import secrets
import string

from sqlalchemy.orm import Session
from . import crud

def create_random_key(length: int = 5) -> str:
    """
    Generate a random key with the specified length using uppercase letters and digits.
    Parameters:
    - length (int): Length of the random key (default is 5)
    Returns:
    - str: Randomly generated key
    """
    chars = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(chars) for _ in range(length))

def create_unique_random_key(db: Session) -> str:
    """
    Generate a unique random key that is not already in use in the database.
    Parameters:
    - db (Session): SQLAlchemy database session
    Returns:
    - str: Unique randomly generated key
    """
    key = create_random_key()
    while crud.get_db_url_by_key(db, key):
        key = create_random_key()
    return key