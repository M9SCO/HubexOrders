import json
from logging import INFO, basicConfig, info
from os import environ

from requests import get, post
from modules.Google.routes.google_routes import *
from requests.structures import CaseInsensitiveDict

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
        "tenantID": tenant_id,
        "tenantMemberID": tenant_member_id
    }
    header = {
        'Authorization': 'Basic '+access_token,
    }
    t = post(url="https://api.hubex.ru/fsm/AUTHZ/Accounts/authorize", headers=header, data=body)
    #r = get("https://api.hubex.ru/fsm/WORK/Tasks/1277")
    print(t.__dict__)
info("app is running!")
