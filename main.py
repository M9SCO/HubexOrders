from logging import INFO, basicConfig

from modules.core.app import app

basicConfig(format='%(levelname)-10s%(message)s  ', level=INFO, )


@app.get("/")
async def main_message():
    return {"message": "Hello world!"}
