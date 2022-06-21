from gspread_asyncio import AsyncioGspreadClientManager

from modules.Google.routes.google_routes import api_set_value
from modules.core.app import app


@app.get("/")
def main_message():
    return {"message": "Hello World"}


print(str(app), "is running!")
