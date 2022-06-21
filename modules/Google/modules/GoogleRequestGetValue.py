
from pydantic import BaseModel


class GoogleRequestGetValue(BaseModel):
    coords: str