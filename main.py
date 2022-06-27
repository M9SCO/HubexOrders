from datetime import datetime
from logging import INFO, basicConfig

import fastapi

from modules.Google.routes.google_routes import *
from modules.Hubex.models.HubexApi import HubexApi

basicConfig(format='%(levelname)-10s%(message)s  ', level=INFO, )


@app.get("/")
async def main_message():
    return {"message": "Hello world!"}


@app.post('/newTask')
async def websoket(r: fastapi.Request):
    task = await r.json()
    task_id = task['TaskID']
    hubex = HubexApi()
    task = await hubex.get_task(task_id)
    full_name = {
        "firstName": task['assignedTo']['firstName'],
        "lastName": task['assignedTo']['lastName'],
        "middleName": task['assignedTo']['middleName']
    }
    d = (full_name["lastName"], full_name["firstName"][0] + "." if full_name["firstName"] else "",
         full_name["middleName"][0] + "." if full_name["middleName"] else "")
    task_model = GoogleRequestPutValues(
        pf_number=str(task['number']),
        object_name=task['asset']['host']['name'],
        tech_object_number="б/н",
        factory_object_number="б/н",
        registration_object_number="б/н",
        location=task['location']['address'],
        customer_name=task['company']['name'],
        date_registration=datetime.fromisoformat(task['timesheet']['created']).strftime("%d.%m.%Y"),
        full_name=" ".join(d)
    )
    await api_put_values(task_model)
    return {"message": "add task"}
