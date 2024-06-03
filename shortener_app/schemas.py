from pydantic import BaseModel

class URLBase(BaseModel):
    """Schema representing base structure of url"""
    target_url: str #url to be shortened

class URL(URLBase):
    """Schema representing shortened url"""
    is_active: bool #indicates whether the shortened url is active
    clicks: int #takes count of the number of times the shortened url has been clicked

    class Config:
        orm_mode = True

class URLInfo(URL):
    """Schema that shows detailed info on shortened url"""
    url: str #shortened url
    admin_url: str #admin url for managing shortened url