from pydantic import BaseModel


class GoogleGetCoords(BaseModel):
    coords: str
