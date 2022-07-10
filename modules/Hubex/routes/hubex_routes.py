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
    attributes = await h.get_attr(task['asset']['id'])
    return {"result": await put_values(agcm=AsyncioGspreadClientManager(get_creds),
                                       r=get_GoogleLogRegistrationPF(task, request.TaskID, asset, attributes))}


@app.post("/api/hubex/task_update")
async def update_task_to_google(request: HubexHookCreateTask):
    h = HubexApi()
    await h._get_access_token()
    task = await h.get_task(request.TaskID)
    asset = await h.get_asset(task['asset']['id'])
    attributes = await h.get_attr(task['asset']['id'])
    return {"result": await update_values(agcm=AsyncioGspreadClientManager(get_creds),
                                          r=get_GoogleLogRegistrationPF(task, request.TaskID, asset, attributes))}


@app.post("/api/hubex/task/{task_id}")
async def get_task(task_id: int):
    print(task_id)
    h = HubexApi()
    await h._get_access_token()
    task = await h.get_task(task_id)
    print(task)
    return task


@app.post("/api/hubex/asset_for_task/{task_id}")
async def get_asset(task_id: int):
    h = HubexApi()
    await h._get_access_token()
    task = await h.get_task(task_id)
    asset = await h.get_asset(task['asset']['id'])
    print(asset)
    return asset


@app.post("/api/hubex/task/checklists/{task_id}")
async def get_checks(task_id: int):
    h = HubexApi()
    await h._get_access_token()
    checklists = await h.get_checklists_task(task_id)
    checklists_keys = checklists.keys()
    hol = [{d["name"]: d["isChecked"] for d in dict(await h.get_checklists_activated(task_id, key)).values()} for
           key in checklists_keys]
    print(hol)
