import json
from logging import INFO, basicConfig, info
from os import environ

from requests import get, post
from modules.Google.routes.google_routes import *
from modules.Google.modules.GoogleRequestPutValues import GoogleRequestPutValues
from datetime import datetime

basicConfig(format='%(levelname)-10s%(message)s  ', level=INFO, )


@app.get("/")
async def main_message():
    data = {
        "serviceToken": environ["TOKEN"].replace("\"", "")
    }
    response = post(url="https://api.hubex.ru/fsm/AUTHZ/AccessTokens", json=data)
    dict = json.loads(response.text)
    access_token = dict['access_token']
    header = {
        'content-type': 'application/json',
        'authorization': 'Bearer ' + access_token,
        'X-Application-ID': '3'
    }
    request_authorize = post(url="https://api.hubex.ru/fsm/AUTHZ/Accounts/authorize", headers=header)
    req_task = get(url="https://api.hubex.ru/fsm/WORK/Tasks/1314", headers=header)
    task = json.loads(req_task.text)
    dict = {
        "firstName": task['assignedTo']['firstName'],
        "lastName": task['assignedTo']['lastName'],
        "middleName": task['assignedTo']['middleName']
    }
    d = (dict["lastName"], dict["firstName"][0] + "." if dict["firstName"] else "", dict["middleName"][0] + "." if dict["middleName"] else "")
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
