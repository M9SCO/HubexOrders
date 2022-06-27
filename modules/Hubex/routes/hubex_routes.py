from gspread_asyncio import AsyncioGspreadClientManager

from modules.Google.src.google_src import get_creds, put_values
from modules.Hubex.models.HubexApi import HubexApi
from modules.Hubex.models.HubexHookCreateTask import HubexHookCreateTask
from modules.Hubex.src.hubex_src import get_GoogleLogRegistrationPF
from modules.core.app import app


@app.post("/api/hubex/task_create")
async def put_newtask_to_google(request: HubexHookCreateTask):
    h = HubexApi()
    task = await h.get_task(request.TaskID)
    return {"result": await put_values(agcm=AsyncioGspreadClientManager(get_creds),
                                       r=get_GoogleLogRegistrationPF(task))}
