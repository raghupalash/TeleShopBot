import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import pprint 

# define the scope
SCOPE = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

def get_sheet(sheet_name: str, sheet_index: int):
    # add credentials to the account
    creds = ServiceAccountCredentials.from_json_keyfile_name('black-messenger-325612-1b2888009503.json', SCOPE)
    # authorize the clientsheet 
    client = gspread.authorize(creds)
    # get the instance of the Spreadsheet
    sheet = client.open('Telegram Shop')
    # get the first sheet of the Spreadsheet
    sheet_instance = sheet.get_worksheet(0)

    return sheet_instance