import secrets
import string

from sqlalchemy.orm import Session
from . import crud

def create_random_key(length: int = 5) -> str:
    """
    Generates a random key of the specified length using uppercase letters and digits.

    Parameters:
    - length (int): Length of the random key (default is 5).

    Returns:
    - str: A randomly generated key consisting of uppercase letters and digits.
    """
    chars = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(chars) for _ in range(length))

def create_unique_random_key(db: Session) -> str:
    """
    Generates a unique random key not already in use in the database.

    Parameters:
    - db (Session): SQLAlchemy database session.

    Returns:
    - str: A unique, randomly generated key.
    
    Notes:
    - Uses the `create_random_key` function to generate a key, then checks the database 
      via the `crud.get_db_url_by_key` function to ensure the key does not already exist.
    """
    key = create_random_key()
    while crud.get_db_url_by_key(db, key):
        key = create_random_key()
    return key