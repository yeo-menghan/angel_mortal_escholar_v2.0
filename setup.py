'''
read from gsheet pairing
all the pairings should be pre-filled on the gsheet
input user_chat_id, angel_chat_id and mortal_chat_id as they /start
use the pairing database for communication between angel / mortal pairings
'''

import os
import db
from dotenv import load_dotenv
load_dotenv() 

from Player import Player
from PlayersMap import PlayersMap

PLAYERS_LEVEL_0 = db.gsheetlvl0comma
PLAYERS_LEVEL_1 = db.gsheetlvl1comma
PLAYERS_LEVEL_2 = db.gsheetlvl2comma

def setup(pl0=PLAYERS_LEVEL_0, pl1=PLAYERS_LEVEL_1, pl2=PLAYERS_LEVEL_2):
    """Sets up players with data structure"""
    pm0 = PlayersMap(pl0)
    pm1 = PlayersMap(pl1)
    pm2 = PlayersMap(pl2)
    return PlayersMap(dict(pm0.get_players_map(), **pm1.get_players_map(), **pm2.get_players_map()))
    # return (
    #     pm1,
    #     pm2,
    #     pm3,
    #     PlayersMap(dict(pm1.get_players_map(), **
    #                pm2.get_players_map(), **pm3.get_players_map()))
    # )


if __name__ == "__main__":
    """Here's an example use case of setup()"""
    print("Running setup.py")
    players = setup(PLAYERS_LEVEL_0, PLAYERS_LEVEL_1, PLAYERS_LEVEL_2)

    [print(i) for i in players.get_players_map().items()]
    player1 = players.get('yeo_menghan')
    print('angel', player1.get_angel().get_username())
    print('mortal', player1.get_mortal().get_username())
