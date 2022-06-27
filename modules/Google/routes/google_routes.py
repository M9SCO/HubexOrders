from gspread_asyncio import AsyncioGspreadClientManager

from modules.Google.modules.GoogleRequestPutValues import GoogleRequestPutValues
from modules.Google.modules.GoogleRequestSetValue import GoogleRequestSetValue
from modules.Google.modules.GoogleRequestGetValue import GoogleRequestGetValue
from modules.Google.src.google_src import set_value, get_creds, get_value, put_values
from modules.core.app import app


@app.post("/api/google")
async def api_set_value(request: GoogleRequestSetValue):
    agcm = AsyncioGspreadClientManager(get_creds)
    return await set_value(agcm=agcm, r=request)


@app.get("/api/google")
async def api_get_value(request: GoogleRequestGetValue):
    agcm = AsyncioGspreadClientManager(get_creds)
    return await get_value(agcm=agcm, r=request)


@app.put("/api/google")
async def api_put_values(request: GoogleRequestPutValues):
    agcm = AsyncioGspreadClientManager(get_creds)
    await put_values(agcm=agcm, r=request)
