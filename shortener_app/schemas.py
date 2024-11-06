#schemas.py

from pydantic import BaseModel

class URLBase(BaseModel):
    """Schema representing the base structure of a URL that needs to be shortened.
    Attributes:
        target_url (str): The original URL that will be shortened.
    """
    target_url: str #url to be shortened

class URL(URLBase):
    """Schema representing a shortened URL with metadata.
    Inherits from URLBase and adds attributes to track the status and usage of the shortened URL.
    """
    is_active: bool #indicates whether the shortened url is active
    clicks: int #takes count of the number of times the shortened url has been clicked

    class Config:
        orm_mode = True

class URLInfo(URL):
    """Schema providing detailed information on a shortened URL, including admin access.
    Inherits from URL and includes additional URLs for user and admin purposes.
    """
    url: str #shortened url
    admin_url: str #admin url for managing shortened url