from typing import List

from pydantic import BaseModel


class GoogleRequestPutValues(BaseModel):
    prefix: str
    date_registration: str
    document_id: str
    date_control: str
    name_object0: str
    object_number_tech: str
    object_number_factory: str
    object_number_registration: str
    customer_name: str
