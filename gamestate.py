from enum import Enum

class GameState:
    def __init__(self, player_count) -> None:
        self.player_count = player_count
        self.__players = []
        self.__states = Enum('GameState', ['WAITING','ONGOING','DONE'])
        self.__state = self.__states['WAITING']

        
    def add_player(self, player_name, conn, addr) -> None:
        try:
            self.__players.append({"name":str(player_name), "conn": conn, "address":addr, "current_score":0, "overall_score":0})
        except:
            raise ValueError("Player name already exist or is invalid")
        
        # existing_players = [entry["name"] for entry in self.__players]
        # if player_name not in existing_players:
        #     try:
        #         self.__players.append({"name":str(player_name), "conn": conn, "address":addr, "current_score":0, "overall_score":0})
        #     except:
        #         raise ValueError("Player name already exist or is invalid")
        # else:
        #     raise ValueError("Player name already exist or is invalid")
            
        
    def remove_player(self, player_name, player_address) -> None:
        for player in self.__players:
            if player["name"] == player_name and player["address"] == player_address:
                self.__players.remove(player)
                return
        raise ValueError("Player not found")
    
    def get_player_names(self) -> list:
        return [entry["name"] for entry in self.__players]
    
    def get_player_names_str(self) -> str:
        return ', '.join(self.get_player_names())