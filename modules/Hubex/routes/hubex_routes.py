from gspread_asyncio import AsyncioGspreadClientManager

from modules.Google.src.google_src import get_creds, put_values, update_values
from modules.Hubex.models.HubexApi import HubexApi
from modules.Hubex.models.HubexHookCreateTask import HubexHookCreateTask
from modules.Hubex.src.hubex_src import get_GoogleLogRegistrationPF
from modules.core.app import app


@app.post("/api/hubex/task_create")
async def put_newtask_to_google(request: HubexHookCreateTask):
    h = HubexApi()
    await h._get_access_token()
    task = await h.get_task(request.TaskID)
    asset = await h.get_asset(task['asset']['id'])
    return {"result": await put_values(agcm=AsyncioGspreadClientManager(get_creds),
                                       r=get_GoogleLogRegistrationPF(task, request.TaskID, asset))}


@app.post("/api/hubex/task_update")
async def update_task_to_google(request: HubexHookCreateTask):
    h = HubexApi()
    await h._get_access_token()
    task = await h.get_task(request.TaskID)
    asset = await h.get_asset(task['asset']['id'])
    return {"result": await update_values(agcm=AsyncioGspreadClientManager(get_creds),
                                          r=get_GoogleLogRegistrationPF(task, request.TaskID, asset))}


@app.post("/api/hubex/task_delete")
async def delete_task_to_google(request: HubexHookCreateTask):
    print(request.TaskID)


@app.post("/api/hubex/task/{task_id}")
async def get_task(task_id: int):
    print(task_id)
    h = HubexApi()
    await h._get_access_token()
    task = await h.get_task(task_id)
    print(task)
    return task
