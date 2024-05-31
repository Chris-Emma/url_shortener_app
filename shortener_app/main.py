from fastapi import FastAPI

app = FastAPI()
"""Instantiating the FastAPI app"""

@app.get('/')
def read_root():
    """Function that returns the '/' route"""
    return "Welcome to the URL shortener"