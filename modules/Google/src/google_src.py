from os import environ

from google.oauth2.service_account import Credentials
from gspread import Worksheet, Cell

from modules.Google.modules.GoogleLogRegistrationPF import GoogleLogRegistrationPF
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


@logging_info_async
async def put_values(agcm, r: GoogleLogRegistrationPF, sheet=environ["SHEET"]):
    agc = await agcm.authorize()
    ss = await agc.open_by_key(sheet)
    zero_ws: Worksheet = await ss.get_worksheet(0)
    table = await zero_ws.get_all_values()
    comparison = {
        '№ п/п': len(table),
        'Номер ПФ': r.pf_number,
        'Наименование объекта': r.object_name,
        'Технологический номер объекта': r.tech_object_number,
        'Заводской номер объекта': r.factory_object_number,
        'Регистрационный номер объекта': r.registration_object_number,
        'Расположение объекта': r.location,
        'Наименование Заказчика\n* выбор из списка': r.customer_name,
        'Дата регистрации документа': r.date_registration,
        'ФИО регистратора\n* выбор из списка': r.full_name,
    }
    results = [comparison.get(cell, "") for cell in table[0]]
    await zero_ws.insert_rows([results], len(table) + 1)
    return results
