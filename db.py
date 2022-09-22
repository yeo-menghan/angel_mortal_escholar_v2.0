import gspread
import json
import os

with open('creds.json', 'w') as f:
    data = json.loads(os.environ.get('GOOGLE_KEY'))
    json.dump(data, f, indent=4)

service_account = gspread.service_account(filename="creds.json") # need to access the file from an env later on alongside the API_KEY for telegram
workbook = service_account.open("angel-mortal-responses")
gsheetresponses = workbook.worksheet("Form Responses 1") # google sheet is linked and working
gsheetlogin = workbook.worksheet("login") # track people who have login
gsheetlvl1names = workbook.worksheet("level_1").col_values(1)
gsheetlvl1 = workbook.worksheet("level_1")
gsheetlvl2names = workbook.worksheet("level_2").col_values(1)
gsheetlvl2 = workbook.worksheet("level_2")
gsheetlvl3names = workbook.worksheet("level_3").col_values(1)
gsheetlvl3 = workbook.worksheet("level_3")

# need to store these values into a single row separated by commas
def commas_list(sheet_list):
    '''Add commas to the given list and deleting the first value'''
    if len(sheet_list) > 0:
        sheet_list.pop(0) # remove first element 'username'
    edited_list = ','.join(sheet_list)
    return edited_list

gsheetlvl1comma = commas_list(gsheetlvl1names)
gsheetlvl2comma = commas_list(gsheetlvl2names)
gsheetlvl3comma = commas_list(gsheetlvl3names)

def get_chat_ids():
    # sheet.update('A6:B6', [['yes', 41929]])
    records = gsheetlogin.get_all_records() # stores in a list of dictionaries
    # print(records)
    chat_ids = {d['user']: d['user_chat_id'] for d in records}
    # print(chat_ids)
    return chat_ids

def update_chat_ids(username, chat_id):
    ''' Used in start_command for player validation'''
    chat_ids = get_chat_ids()
    chat_ids[username] = int(chat_id) 
    # search user column (column A) for username
    cell = gsheetlogin.find(username, in_column=1)
    # update user_chat_id (same row, col+1)
    gsheetlogin.update_cell(cell.row, cell.col + 1, chat_ids[username])
    # gsheetlogin.update("A2", [[key, value]
    #              for key, value in sorted(chat_ids.items())])
    # update playerdict
    # create_playerdict(gsheetlvl1)
    # create_playerdict(gsheetlvl2)
    return chat_ids


def create_playerdict(sheet):
    '''Retrieve mortal's information to be disseminated to the angel
    '''
    records = sheet.get_all_records()
    # convert form list of dictionaries to dictionary of dictionaries
    new_dict = {}
    for item in records:
        user = item['username']
        new_dict[user] = item
    # print(new_dict)
    return new_dict

# TODO: get_all_information() to prepare information from Form Responses 1 and tidy them up into a presentable format

# TODO: Function to update angel_chat_id and mortal_chat_id from user_chat_id
# can be done manually on the google sheet or iteratively here by scraping through the sheet and updating when matched via name


PLAYER_LVL1_INFO = create_playerdict(gsheetlvl1)
PLAYER_LVL2_INFO = create_playerdict(gsheetlvl2)

#Combine information for both lvl1 and lvl2 google sheet
def Merge(dict1, dict2):
    res = {**dict1, **dict2}
    return res

PLAYER_COMBINED_INFO = Merge(PLAYER_LVL1_INFO, PLAYER_LVL2_INFO)
