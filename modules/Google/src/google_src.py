from os import environ

from google.oauth2.service_account import Credentials
from gspread import Worksheet, Cell


def get_creds():
    creds = Credentials.from_service_account_file("resources/google/key.json")
    scoped = creds.with_scopes([
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ])
    return scoped


async def set_value(agcm, coords, value, sheet=environ["SHEET"]):
    agc = await agcm.authorize()

    ss = await agc.open_by_key(sheet)
    zero_ws: Worksheet = await ss.get_worksheet(0)
    cell: Cell = Cell.from_address(coords)
    return await zero_ws.update_cell(cell.row, cell.col, value)


async def get_value(agcm, coords, sheet=environ["SHEET"]):
    agc = await agcm.authorize()

    ss = await agc.open_by_key(sheet)
    zero_ws: Worksheet = await ss.get_worksheet(0)
    return await zero_ws.get_values(coords)
