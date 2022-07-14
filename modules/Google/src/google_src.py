from datetime import datetime
from os import environ

from google.oauth2.service_account import Credentials
from gspread import Worksheet, Cell
from gspread_asyncio import AsyncioGspreadClientManager

from modules.Google.modules.GoogleLogRegistrationPF import GoogleLogRegistrationPF
from modules.core.logger import logging_info, logging_info_async


@logging_info
def get_creds():
    creds = Credentials.from_service_account_file("resources/google/key.json")
    scoped = creds.with_scopes([
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
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
    await zero_ws.add_rows(1)
    comparison = {
        '№ п/п': len(table),
        'Номер ПФ': r.pf_number,
        'ERPID': r.erp_id,
        'Номер заявки': r.task_id,
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


@logging_info_async
async def update_values(agcm, r: GoogleLogRegistrationPF, sheet=environ["SHEET"]):
    agc = await agcm.authorize()
    ss = await agc.open_by_key(sheet)
    zero_ws: Worksheet = await ss.get_worksheet(0)
    table = await zero_ws.get_all_values()
    task_id_col_numb = table[0].index('Номер заявки')
    task_id_list = [table[i][task_id_col_numb] for i in range(len(table))]
    task_row_number = task_id_list.index(str(r.task_id))
    comparison = {
        '№ п/п': task_row_number,
        'Номер ПФ': r.pf_number,
        'ERPID': r.erp_id,
        'Номер заявки': r.task_id,
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
    await zero_ws.update(f"A{task_row_number + 1}", [results])
    return results


@logging_info_async
async def put_workready_to_table(agcm: AsyncioGspreadClientManager,
                                 table_name: str,
                                 object_name: str,
                                 title_name: str,
                                 work_name: str,
                                 perpetrator: str) -> None:
    agc = await agcm.authorize()
    ss = await agc.open(table_name)
    zero_ws: Worksheet = await ss.get_worksheet(0)
    f, s, t, *objects = await zero_ws.get_all_values()
    start_col_num = f.index(f"{title_name}")
    end_col_num = start_col_num
    for i in range(start_col_num + 1, len(f)):
        if len(f[i]) == 0:
            end_col_num += 1
        else:
            break
    end_col_num += 1
    start_col_num += 1
    # started = next((n for n, column in enumerate(t, 1) if column in ("Дата", "Фамилия")))
    cursor = s[start_col_num]
    works = {}
    for n, column in enumerate(s[start_col_num - 1:], start_col_num - 1):
        if n != end_col_num:
            if column:
                cursor = column
                works[cursor] = {}
            works[cursor][t[n]] = n + 1
        else:
            break
    work = works[work_name]
    # obj = next(n for n, ob in enumerate((objects[next(n for n, ob in enumerate)]), 1))
    names_col = next(_ for _, col in enumerate(f) if col == "Наименование")
    row, name = next(el for el in [(n, name[names_col]) for n, name in enumerate(objects, 4)] if el[1] == object_name)
    putted_value = [
        {"range": f"r{row}c{work['Дата']}",
         "values": [[datetime.now().strftime("%d.%m.%Y")]]},
        {"range": f"r{row}c{work['Фамилия']}",
         "values": [[perpetrator]]},
    ]

    return await zero_ws.batch_update(data=putted_value)
