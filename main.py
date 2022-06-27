from logging import INFO, basicConfig

from modules.Google.routes.google_routes import *

basicConfig(format='%(levelname)-10s%(message)s  ', level=INFO, )


@app.get("/")
async def main_message():
    return {"message": "Hello world!"}