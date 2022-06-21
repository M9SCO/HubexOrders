from os import environ
from typing import List

from google.oauth2.service_account import Credentials
from gspread import Worksheet, Cell
from pydantic import parse_obj_as, BaseModel

from modules.Google.modules.GoogleRequestPutValues import GoogleRequestPutValues

from modules.core.logger import logging_info, logging_info_async


@logging_info
def get_creds():
    creds = Credentials.from_service_account_file("resources/google/key.json")
    scoped = creds.with_scopes([
        "https://www.googleapis.com/auth/spreadsheets"
    ])
    return scoped

@logging_info_async
async def set_value(agcm, r, sheet=environ["SHEET"]):
    agc = await agcm.authorize()

    ss = await agc.open_by_key(sheet)
    zero_ws: Worksheet = await ss.get_worksheet(0)
    cell: Cell = Cell.from_address(r.coords)
    return await zero_ws.update_cell(cell.row, cell.col, r.value)

@logging_info_async
async def get_value(agcm, r, sheet=environ["SHEET"]):
    agc = await agcm.authorize()

    ss = await agc.open_by_key(sheet)
    zero_ws: Worksheet = await ss.get_worksheet(0)
    return await zero_ws.get_values(r.coords)


async def put_values(agcm, r, sheet=environ["SHEET"]):
    agc = await agcm.authorize()
    ss = await agc.open_by_key(sheet)
    zero_ws: Worksheet = await ss.get_worksheet(0)
    count = len(await zero_ws.col_values(1))
    return await zero_ws.append_row([count, r.prefix, r.date_registration, r.document_id, r.date_control, r.name_object0,
                                     r.object_number_tech, r.object_number_factory,
                                     r.object_number_registration, r.customer_name])
