from gspread_asyncio import AsyncioGspreadClientManager

from modules.Google.modules.GoogleGetCoords import GoogleGetCoords
from modules.Google.modules.GoogleLogRegistrationPF import GoogleLogRegistrationPF
from modules.Google.modules.GoogleSetWithCoords import GoogleSetWithCoords
from modules.Google.src.google_src import set_value, get_creds, get_value, put_values, put_workready_to_table
from modules.core.app import app


@app.post("/api/google")
async def api_set_value(request: GoogleSetWithCoords):
    agcm: AsyncioGspreadClientManager = AsyncioGspreadClientManager(get_creds)
    return await set_value(agcm=agcm, r=request)


@app.get("/api/google")
async def api_get_value(request: GoogleGetCoords):
    agcm: AsyncioGspreadClientManager = AsyncioGspreadClientManager(get_creds)
    return await get_value(agcm=agcm, r=request)


@app.put("/api/google")
async def api_put_values(request: GoogleLogRegistrationPF):
    agcm: AsyncioGspreadClientManager = AsyncioGspreadClientManager(get_creds)
    await put_values(agcm=agcm, r=request)


@app.get("/api")
async def set_with():
    agcm: AsyncioGspreadClientManager = AsyncioGspreadClientManager(get_creds)
    return await put_workready_to_table(agcm=agcm,
                                        table_name="АО «Волгогаз»",
                                        title_name="ЧЕК-ЛИСТ НА ПОДЗЕМНЫЙ ГАЗОПРОВОД",
                                        object_name="Тестовый газопровод",
                                        work_name="Проверка эффективности работы ЭХЗ",
                                        perpetrator="Чернов Г. И.")
