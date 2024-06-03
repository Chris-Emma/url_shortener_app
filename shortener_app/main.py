import secrets
import validators
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import models, schemas
from .database import SessionLocal, engine
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()
"""Instantiating the FastAPI app"""

def raise_bad_request(message):
    """Raises an exception error if url provided isnt valid"""
    raise HTTPException(status_code=400, detail=message)

@app.get('/')
def read_root():
    """Function that returns the '/' route"""
    return "Welcome to the URL shortener"

@app.post("/url", response_model=schemas.URLInfo)
def create_url(url: schemas.URLBase):
    """
    Endpoint to create shortened url
    Parameters:
        -url schemas.URLBase: pydantic model representing url to be shortened
    Returns:
        -str indicating url to be shortened should be a string
    Raises:
        -HTTPException: if the provided URL is invalid 
    """
    #validates provided url using Validators module
    if not validators.url(url.target_url):
        raise_bad_request(message="The provided url is invalid")

        chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        key = "".join(secrets.choice(chars) for _ in range(5))
        secret_key = "".join(secrets.choice(chars) for _ in range(8))
        db_url = models.URL(
            target_url=url.target_url, key=key, secret_key=secret_key
        )
        db.add(db_url)
        db.commit()
        db.refresh(db_url)
        db_url.url = key
        db_url.admin_url = secret_key
        
        return db_url