import json
from logging import INFO, basicConfig, info
from os import environ

from requests import get, post
from modules.Google.routes.google_routes import *
basicConfig(format='%(levelname)-10s%(message)s  ', level=INFO, )


@app.get("/")
def main_message():
    data = {
        "serviceToken": environ["TOKEN"].replace("\"", "")
    }
    r = post(url="https://api.hubex.ru/fsm/AUTHZ/AccessTokens", json=data)
    dict = json.loads(r.text)
    access_token = dict['access_token']
    tenant = dict['tenant']
    tenant_id = tenant['id']
    tenant = dict['tenantMember']
    tenant_member_id = tenant['id']
    body = {
        'content-type': 'application/json',
        'tenantID': tenant_id,
        'tenantMemberID':tenant_member_id
    }
    header = {
        'content-type':'application/json',
        'authorization': 'Bearer '+access_token,
        'X-Application-ID': '3'
    }
    req1 = post(url="https://api.hubex.ru/fsm/AUTHZ/Accounts/authorize", headers=header, data=body)
    req2 = get(url="https://api.hubex.ru/fsm/WORK/Tasks/1277", headers=header)
    print(req2.json())