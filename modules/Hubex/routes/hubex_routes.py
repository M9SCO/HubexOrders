from modules.core.app import app
from fastapi import Request

@app.get("/hubex/")
async def get_order(request: Request):
    print(request.__dict__)