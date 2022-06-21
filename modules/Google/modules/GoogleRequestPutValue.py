from typing import Union

from pydantic import BaseModel


class GoogleRequestPutValue(BaseModel):
    coords: str
    value: Union[str, list[str]]