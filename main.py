from logging import INFO, basicConfig

from modules.core.app import app
from save_imports import __all__

basicConfig(format='%(levelname)-10s%(message)s  ', level=INFO, )


@app.get("/")
async def main_message():
    return {"message": "Hello world!"}
