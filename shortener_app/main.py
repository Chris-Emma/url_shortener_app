import validators
from fastapi import FastAPI, HTTPException

from . import schemas

app = FastAPI()
"""Instantiating the FastAPI app"""

def raise_bad_request(message):
    """Raises an exception error if url provided isnt valid"""
    raise HTTPException(status_code=400, detail=message)

@app.get('/')
def read_root():
    """Function that returns the '/' route"""
    return "Welcome to the URL shortener"

@app.post("/url")
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
        return f"TODO: Create database entry for {url.target_url}"