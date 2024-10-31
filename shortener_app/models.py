from sqlalchemy import Boolean, Column, Integer, String
from .database import Base

class URL(Base):
    """
    SQLAlchemy model representing a URL entry in the database.
    Attributes:
    - id (int): Primary key for the URL entry.
    - key (str): Unique key for the shortened URL, indexed for fast lookups.
    - secret_key (str): Unique secret key for managing the URL, indexed for fast lookups.
    - target_url (str): The original URL that is being shortened, indexed for fast lookups.
    - is_active (bool): Boolean flag indicating if the URL entry is active (default is True).
    - clicks (int): Count of how many times the shortened URL has been accessed (default is 0).
    """
    __tablename__ = "urls" # this is the name of table in this database model

    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True, index=True)
    secret_key = Column(String, unique=True, index=True)
    target_url = Column(String, index=True)
    is_active = Column(Boolean, default=True)
    clicks = Column(Integer, default=0)