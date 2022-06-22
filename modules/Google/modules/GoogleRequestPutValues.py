from pydantic import BaseModel


class GoogleRequestPutValues(BaseModel):
    pf_number: str
    object_name: str
    tech_object_number: str
    factory_object_number: str
    registration_object_number: str
    location: str
    customer_name: str
    date_registration: str
    full_name: str