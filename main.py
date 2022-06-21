from logging import INFO, basicConfig, info

from modules.core.app import app
from modules.Google.routes.google_routes import *
basicConfig(format='%(levelname)-10s%(message)s  ', level=INFO, )



@app.get("/")
def main_message():
    return {"message": "Hello World"}

info("app is running!")
