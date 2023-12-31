from copy import deepcopy
    
class Game:
    def __init__(self, id, player_size, category):
        self.QnA = []
        self.started = False
        self.category = category
        self.round_scores_count = 0 # How many players sent their score at the end of a round
        self.rounds = [0 for _ in range (10)]   # 0: not finished, 1: finished
        self.id = id
        self.player_size = int(player_size)     # chosen during the game's creation

        # each key is a player id (their ipv4), and the corresponding 
        # value is another dictionary containing the player's info
        self.players: dict[str,dict] = {}   
    
    def has_started(self):
        return self.started
    
    def add_player(self, player_id, name):
        self.players[player_id] = {'name': name, 'score': 0, 'received_count': 0}

    def get_category(self):
        return self.category
    
    def get_player_count(self):
        return len(self.players)
    
    def get_player_size(self):
        return self.player_size
    
    def get_id(self):
        return self.id
    
    def get_players(self):
        return self.players
    
    def get_players_except(self, ip):
        players_copy = deepcopy(self.players)
        del players_copy[ip]
        return players_copy

    def set_qna(self, QnA): 
        self.QnA = QnA

    def set_start(self):
        self.started = True
        
    def delete_player(self, ip):
        del self.players[ip]
        
    def get_qna_length(self):
        return len(self.QnA)

    def get_qna(self):
        return self.QnA
    
    def update_score(self, ip, score, index):
        self.players[ip]['score'] += score
        self.round_scores_count += 1
        if self.round_scores_count >= self.get_player_count():
            self.round_scores_count = 0
            self.rounds[index] = 1

    def is_round_finished(self, index):
        return self.rounds[index]
        
    def get_received_count(self, ip):
        return self.players[ip]['received_count']
    
    def reset_received_count(self, ip):
        self.players[ip]['received_count'] = 0

    def increment_received_count(self, ip):
        self.players[ip]['received_count'] += 1

    def get_highest_scorer(self):
        highest_score = max(player['score'] for player in self.players.values())
        top_players = [player_data['name'] for player_id, player_data in self.players.items() if player_data['score'] == highest_score]
        return top_players
    