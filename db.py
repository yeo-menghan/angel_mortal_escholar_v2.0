# currently using the previous google sheet to test new features

import gspread
import json
import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

with open('creds.json', 'w') as f:
    google_key = json.loads(os.environ.get('GOOGLE_KEY'))
    # print(google_key)  # Debugging line
    json.dump(google_key, f, indent=4)

service_account = gspread.service_account(filename="creds.json")
workbook = service_account.open("angel-mortal-responses")
gsheetresponses = workbook.worksheet("Form Responses 1") # google sheet is linked and working
gsheet_overview = workbook.worksheet("overview") # track people who have login and last messages
gsheetlvl0names = workbook.worksheet("level_0").col_values(1)
gsheetlvl0 = workbook.worksheet("level_0")
gsheetlvl1names = workbook.worksheet("level_1").col_values(1)
gsheetlvl1 = workbook.worksheet("level_1")
gsheetlvl2names = workbook.worksheet("level_2").col_values(1)
gsheetlvl2 = workbook.worksheet("level_2")

# need to store these values into a single row separated by commas
def commas_list(sheet_list):
    '''Add commas to the given list and deleting the first value'''
    if len(sheet_list) > 0:
        sheet_list.pop(0) # remove first element 'username'
    edited_list = ','.join(sheet_list)
    return edited_list

# comma lists are used in setup.py
gsheetlvl0comma = commas_list(gsheetlvl0names)
gsheetlvl1comma = commas_list(gsheetlvl1names)
gsheetlvl2comma = commas_list(gsheetlvl2names)

def get_chat_ids():
    records = gsheet_overview.get_all_records() # stores in a list of dictionaries
    chat_ids = {d['user']: d['user_chat_id'] for d in records}
    return chat_ids

# def update_chat_ids(username, chat_id):
#     ''' Used in start_command for player validation'''
#     chat_ids = get_chat_ids()
#     chat_ids[username] = int(chat_id)
#     print(f"Searching for username: {username}")
#     cell = gsheet_overview.find(username, in_column=1)     # search user column (column A) for username
#     if cell is None:
#         print(f"Username '{username}' not found in Google Sheet.")
#         return chat_ids  # or handle it according to your application logic
#     gsheet_overview.update_cell(cell.row, cell.col + 1, chat_ids[username])     # update user_chat_id (same row, col+1)
#     return chat_ids

def update_chat_ids(username, chat_id):
    ''' Used in start_command for player validation'''
    chat_ids = get_chat_ids()
    chat_ids[username] = int(chat_id)
    print(f"Searching for username: {username}")
    cell = gsheet_overview.find(username, in_column=1)  # search user column (column A)

    if cell is None:
        print(f"Username '{username}' not found in Google Sheet.")
        return chat_ids  # or handle as needed

    gsheet_overview.update_cell(cell.row, cell.col + 1, chat_ids[username])  # update user_chat_id (same row, col+1)
    return chat_ids


def create_playerdict(sheet):
    '''Retrieve mortal's information to be disseminated to the angel'''
    records = sheet.get_all_records()
    # convert form list of dictionaries to dictionary of dictionaries
    new_dict = {}
    for item in records:
        user = item['username']
        new_dict[user] = item
    return new_dict


'''Track time of last sent msg of user as angel and mortal'''
now = datetime.now()
formatted_now = now.strftime("%m/%d/%Y %H:%M:%S")

# update the last seen timing of individual under "overview" page
def update_timing_mortal(username):
    cell = gsheet_overview.find(username, in_column=1)
    # last_seen_mortal is column +2 from username, update cell to current date and time
    gsheet_overview.update_cell(cell.row, cell.col + 2, formatted_now)

def update_timing_angel(username):
    cell = gsheet_overview.find(username, in_column=1)
    # last_seen_angel is column +3 from username, update cell to current date and time
    gsheet_overview.update_cell(cell.row, cell.col + 3, formatted_now)


'''Combine information for both lvl0, lvl1 and lvl2 google sheet'''
PLAYER_LVL0_INFO = create_playerdict(gsheetlvl0)
PLAYER_LVL1_INFO = create_playerdict(gsheetlvl1)
PLAYER_LVL2_INFO = create_playerdict(gsheetlvl2)

def Merge(dict0, dict1, dict2,):
    res = {**dict0, **dict1, **dict2}
    return res

PLAYER_COMBINED_INFO = Merge(PLAYER_LVL0_INFO, PLAYER_LVL1_INFO, PLAYER_LVL2_INFO)
