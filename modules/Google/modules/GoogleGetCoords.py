from pydantic import BaseModel


class GoogleGetCoords(BaseModel):
    coords: str

class GoogleGetCoordsName(BaseModel):
    coords: str
    name: str
