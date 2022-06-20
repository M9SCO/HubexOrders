from gspread_asyncio import AsyncioGspreadClientManager

from modules.Google.src.google_src import set_value, get_creds

from asyncio import run

agcm = AsyncioGspreadClientManager(get_creds)
run(set_value("K1", "Перемен для ", agcm))

