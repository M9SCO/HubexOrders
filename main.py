from logging import INFO, basicConfig

from modules.Google.routes.google_routes import api_set_value, api_get_value, api_put_values
from modules.Hubex.routes.hubex_routes import put_newtask_to_google
from modules.core.app import app

__all__ = (
    "api_set_value",
    "api_get_value",
    "api_put_values",
    "put_newtask_to_google"
)

basicConfig(format='%(levelname)-10s%(message)s  ', level=INFO, )


@app.get("/")
async def main_message():
    return {"message": "Hello world!"}
