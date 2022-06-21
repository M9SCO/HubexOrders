from gspread_asyncio import AsyncioGspreadClientManager

from modules.Google.modules.GoogleRequestPutValue import GoogleRequestPutValue
from modules.Google.src.google_src import set_value, get_creds
from modules.core.app import app


@app.post("/api/google")
async def api_set_value(request: GoogleRequestPutValue):
    agcm = AsyncioGspreadClientManager(get_creds)
    print(request)
    await set_value(agcm=agcm, coords=request.coords, value=request.value)