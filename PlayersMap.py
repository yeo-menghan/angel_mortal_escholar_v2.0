from Player import Player
class PlayersMap:
    def __init__(self, players):
        if players:
            if type(players) is str:
                players = self.get_players_from_string(players)
                self.players_map = {
                    player.get_username(): player for player in players}
            elif type(players) is list:
                self.players_map = {
                    player.get_username(): player for player in players}
            elif type(players) is dict:
                self.players_map = players.copy()
            else:
                raise TypeError(
                    "Only strings, lists, or dictionaries are allowed.")
        else:
            raise AssertionError("Players cannot be empty!")

    def get_players_map(self):
        """Returns a copy such that the original dict is not mutated"""
        return self.players_map.copy()

    def get_players_from_string(self, players_string):
        players_list = players_string.split(",")
        return self.get_players_from_list(players_list)

    def get_players_from_list(self, players_list):
        players = [Player(username) for username in players_list]
        for i in range(len(players)):
            players[i].set_angel_mortal(
                players[(i+1) % len(players)],
                players[i-1]
            )
        return players

    def get(self, username):
        return self.players_map.get(username)
