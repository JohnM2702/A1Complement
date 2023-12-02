class Game:
    def __init__(self, id, player_size):
        # self.type = ''    # image / trivia
        self.QnA = []
        self.started = False
        self.went = []      # Track if each player guessed
        self.id = id
        self.guesses = []
        self.player_size = int(player_size)

        # each key is a player id (their ipv4), and the corresponding 
        # value is another dictionary with 'name' and 'score' keys
        self.players: dict[str,dict] = {}   
    
    def has_started(self):
        return self.started
    
    def add_player(self, player_id, name, score):
        self.players[player_id] = {'name': name, 'score': score}

    def get_player(self, player_id):
        return self.players.get(player_id, None)
    
    def get_player_count(self):
        return len(self.players)
    
    def get_player_size(self):
        return self.player_size
    
    def get_id(self):
        return self.id
    
    def get_players(self):
        return self.players

    def set_qna(self, QnA): 
        self.QnA = QnA

    def set_start(self):
        self.started = True
