from os import environ

from google.oauth2.service_account import Credentials


# import httplib2


# from googleapiclient.discovery import build
# from oauth2client.service_account import ServiceAccountCredentials

# sync

# def google_execute():
#     key = 'resources/google/key.json'
#     scopes = ['https://www.googleapis.com/auth/spreadsheets']
#
#     creds_service = ServiceAccountCredentials.from_json_keyfile_name(key, scopes).authorize(httplib2.Http())
#     service =  build('sheets', 'v4', http=creds_service)
#
#
#     SAMPLE_SPREADSHEET_ID = '1AQPfo4twK-R0HUop3bgOB4DFCWkJA48EP-NRd2GismI'
#     SAMPLE_RANGE_NAME = 'Лист1!A1:J99'
#
#
#
#     sheet = service.spreadsheets()
#     result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute()
#     values = result.get('values', [])
#     print(values)

# Me

def get_creds():
    # To obtain a service account JSON file, follow these steps:
    # https://gspread.readthedocs.io/en/latest/oauth2.html#for-bots-using-service-account

    creds = Credentials.from_service_account_file("resources/google/key.json")
    scoped = creds.with_scopes([
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ])
    return scoped


async def set_value(agcm, coord, value):
    agc = await agcm.authorize()

    ss = await agc.open_by_key(environ["SHEET"])
    ws = await ss.add_worksheet("My Test Worksheet", 10, 5)
    return await ws.update_cell(coord, value)
