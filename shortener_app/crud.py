from sqlalchemy.orm import Session
from . import keygen, models, schemas

def create_db_url(db: Session, url: schemas.URLBase) -> models:
    """
    Creates a new URL entry in the database with a unique key and secret key.
    Parameters:
    - db (Session): SQLAlchemy database session.
    - url (URLBase): Schema representing the URL to be shortened.
    Returns:
    - models.URL: The newly created URL entry in the database.
    """
    key = keygen.create_unique_random_key(db)
    secret_key = f"{key}_{keygen.create_random_key(length=8)}"
    db_url = models.URL(
        target_url=url.target_url, key=key, secret_key=secret_key
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url

def get_db_url_by_key(db: Session, url_key:str) -> models.URL:
    """
    Retrieves an active URL entry from the database based on the provided key.
    Parameters:
    - db (Session): SQLAlchemy database session.
    - url_key (str): The key associated with the URL entry to retrieve.
    Returns:
    - models.URL: The URL entry with the specified key, or None if not found or inactive.
    """
    return (
        db.query(models.URL)
        .filter(models.URL.key == url_key, models.URL.is_active)
        .first()
    )

def get_db_url_by_secret_key(db: Session, secret_key: str) -> models.URL:
    """
    Retrieves an active URL entry from the database using the secret key.
    Parameters:
    - db (Session): SQLAlchemy database session.
    - secret_key (str): The secret key associated with the URL entry to retrieve.
    Returns:
    - models.URL: The URL entry with the specified secret key, or None if not found or inactive.
    """
    return (
        db.query(models.URL)
        .filter(models.URL.secret_key == secret_key, models.URL.is_active)
        .first()
    )

def update_db_clicks(db: Session, db_url: schemas.URL) -> models.URL:
    """
    Increments the click count for a specific URL entry in the database.
    Parameters:
    - db (Session): SQLAlchemy database session.
    - db_url (URL): The URL entry for which to update the click count.
    Returns:
    - models.URL: The updated URL entry with the incremented click count.
    """
    db_url.clicks += 1
    db.commit()
    db.refresh(db_url)
    return db_url

def deactivate_db_url_by_secret_key(db: Session, secret_key: str) -> models.URL:
    """
    Deactivates a URL entry in the database based on the secret key.
    Parameters:
    - db (Session): SQLAlchemy database session.
    - secret_key (str): The secret key associated with the URL entry to deactivate.
    Returns:
    - models.URL: The deactivated URL entry, or None if not found.
    """
    db_url = get_db_url_by_secret_key(db, secret_key)
    if db_url:
        db_url.is_active = False
        db.commit()
        db.refresh(db_url)

    return db_url