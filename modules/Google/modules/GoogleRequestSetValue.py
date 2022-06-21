from typing import Union

from pydantic import BaseModel


class GoogleRequestSetValue(BaseModel):
    coords: str
    value: Union[str, list[str], list[list[str]]]