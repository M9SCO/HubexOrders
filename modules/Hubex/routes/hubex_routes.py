from gspread_asyncio import AsyncioGspreadClientManager

from modules.Google.src.google_src import get_creds, put_values, update_values, put_workready_to_table, \
    get_works_from_table
from modules.Hubex.models.HubexApi import HubexApi
from modules.Hubex.models.HubexHookCreateTask import HubexHookCreateTask
from modules.Hubex.src.hubex_src import get_GoogleLogRegistrationPF, full_name
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
    h = await HubexApi.create()
    task = await h.get_task(request.TaskID)
    asset = await h.get_asset(task['asset']['id'])
    attributes = await h.get_attr(task['asset']['id'])
    return {"result": await update_values(agcm=AsyncioGspreadClientManager(get_creds),
                                          r=get_GoogleLogRegistrationPF(task, request.TaskID, asset, attributes))}


@app.post("/api/hubex/checklists_update")
async def update_task_to_google(request: HubexHookCreateTask):
    h = await HubexApi.create()
    task = await h.get_task(request.TaskID)
    table_name = task['company']['name']
    object_name = task['asset']['name']
    checklists_names = await h.get_checklists_task(request.TaskID)
    checklists_keys = checklists_names.keys()
    checklists = {checklists_names[key]['checkList']['name']:
                      {d["name"]: d["isChecked"] for d in dict(
                          await h.get_checklists_activated(request.TaskID, key)).values()} for key in checklists_keys}
    result = {}
    for key in checklists:
        try:
            checklists_from_hubex = checklists[key]
            checklists_from_table = await get_works_from_table(agcm=AsyncioGspreadClientManager(get_creds),
                                                               table_name=table_name, object_name=object_name,
                                                               title_name=key)
            for nextkey in checklists_from_hubex:
                if checklists_from_hubex[nextkey] != checklists_from_table[nextkey]:
                    result[key] = await put_workready_to_table(agcm=AsyncioGspreadClientManager(get_creds),
                                                               table_name=table_name,
                                                               object_name=object_name, title_name=key,
                                                               work_name=nextkey,
                                                               status=bool(checklists_from_hubex[nextkey]),
                                                               perpetrator=full_name(task.get('assignedTo')))
        except ValueError:
            continue
    return {"result": result}


@app.post("/api/hubex/task/{task_id}")
async def get_task(task_id: int):
    h = await HubexApi.create()
    await h._get_access_token()
    return await h.get_task(task_id)


@app.post("/api/hubex/asset_for_task/{task_id}")
async def get_asset(task_id: int):
    h = await HubexApi.create()
    task = await h.get_task(task_id)
    return await h.get_asset(task['asset']['id'])


@app.post("/api/hubex/task/checklists/{task_id}")
async def get_checks(task_id: int):
    h = await HubexApi.create()
    checklists = await h.get_checklists_task(task_id)
    checklists_keys = checklists.keys()
    print({checklists[key]['checkList']['name']: {d["name"]: d["isChecked"] for d in
                                                  dict(await h.get_checklists_activated(task_id, key)).values()} for
           key in checklists_keys})
    return {checklists[key]['checkList']['name']: {d["name"]: d["isChecked"] for d in
                                                   dict(await h.get_checklists_activated(task_id, key)).values()} for
            key in checklists_keys}
