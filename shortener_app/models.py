from sqlalchemy import Boolean, Column, Integer, String
from .database import Base

class URL(Base):
    """SQLAlchemy model representing a url in the database"""
    __tablename__ = "urls" #name of table in this database model

    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True, index=True)
    secret_key = Column(String, unique=True, index=True)
    target_url = Column(String, index=True)
    is_active = Column(Boolean, default=True)
    clicks = Column(Integer, default=0)