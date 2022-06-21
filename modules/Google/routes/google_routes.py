from gspread_asyncio import AsyncioGspreadClientManager

from modules.Google.modules.GoogleRequestPutValue import GoogleRequestPutValue
from modules.Google.modules.GoogleRequestGetValue import GoogleRequestGetValue
from modules.Google.src.google_src import set_value, get_creds, get_value
from modules.core.app import app


@app.post("/api/google")
async def api_set_value(request: GoogleRequestPutValue):
    agcm = AsyncioGspreadClientManager(get_creds)
    print(request)
    await set_value(agcm=agcm, coords=request.coords, value=request.value)

@app.get("/api/google")
async def api_get_value(request: GoogleRequestGetValue):
    agcm = AsyncioGspreadClientManager(get_creds)
    print(request)
    await get_value(agcm=agcm, coords=request.coords)
