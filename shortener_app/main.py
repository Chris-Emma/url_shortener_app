import validators
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from starlette.datastructures import URL

from . import crud, models, schemas
from .database import SessionLocal, engine
models.Base.metadata.create_all(bind=engine)
from .config import get_settings

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()
"""Instantiating the FastAPI ap"""

def raise_bad_request(message):
    """Raises an exception error if url provided is not valid"""
    raise HTTPException(status_code=400, detail=message)

def raise_not_found(request):
    """Raises an exception if the requested url is not found"""
    message = f"URL '{request.url}' doesn't exist"
    raise HTTPException(status_code=404, detail=message)
@app.get('/')
def read_root():
    """Function that returns the '/' route"""
    return "Welcome to the URL shortener"

@app.post("/url", response_model=schemas.URLInfo)
def create_url(url: schemas.URLBase, db: Session = Depends(get_db)):
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
    db_url = crud.create_db_url(db=db, url=url)
    return get_admin_info(db_url)

    # db_url.url = db_url.key
    # db_url.admin_url = db_url.secret_key

    # chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    # key = "".join(secrets.choice(chars) for _ in range(5))
    # secret_key = "".join(secrets.choice(chars) for _ in range(8))

    # db.add(db_url)
    # db.commit()
    # db.refresh(db_url)
    # db_url.url = key
    # db_url.admin_url = secret_key
        
    # return db_url

@app.get("/{url_key}")
#Forwards shortened url to target url
def forward_to_target_url(
        url_key: str,
        request: Request,
        db: Session = Depends(get_db)
    ):
    # db_url = (
    #     db.query(models.URL)
    #     .filter(models.URL.key == url_key, models.URL.is_active)
    #     .first()
    # )
    if db_url:= crud.get_db_url_by_key(db=db, url_key=url_key):
        crud.update_db_clicks(db=db, db_url=db_url)
        return RedirectResponse(db_url.target_url)
    else:
        raise_not_found(request)

@app.get(
    "/admin/{secret_key}",
    name="administration info",
    response_model=schemas.URLInfo,
)
def get_url_info(
    secret_key: str, request: Request, db: Session = Depends(get_db)
):
    if db_url := crud.get_db_url_by_secret_key(db, secret_key=secret_key):
        return get_admin_info(db_url)
        # db_url.url = db_url.key
        # db_url.admin_url = db_url.secret_key
        # return db_url
    else:
        raise_not_found(request)

def get_admin_info(db_url: models.URL) -> schemas.URLInfo:
    base_url = URL(get_settings().base_url)
    admin_endpoint = app.url_path_for(
        "administration info", secret_key=db_url.secret_key
    )
    db_url.url = str(base_url.replace(path=db_url.key))
    db_url.admin_url = str(base_url.replace(path=admin_endpoint))
    return db_url

@app.delete("/admin/{secret_key}")
def delete_url(
    secret_key: str, request: Request, db: Session = Depends(get_db)
):
    if db_url := crud.deactivate_db_url_by_secret_key(db, secret_key=secret_key):
        message = f"Successfully deleted shortened URL for '{db_url.target_url}'"
        return {"detail": message}
    else:
        raise_not_found(request)