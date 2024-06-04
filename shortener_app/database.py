from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import get_settings

#create SQLAlchemy engine to connect to the database
engine = create_engine(
    get_settings().db_url, connect_args={"check_same_thread": False}
)

#create a session maker to generate databse sessions
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

#create a Base class for declarative class definitions
Base = declarative_base()