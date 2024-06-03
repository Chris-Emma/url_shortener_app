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
    
    """