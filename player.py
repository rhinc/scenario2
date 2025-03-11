class Player:
    def __init__(self):
        self.score = 0

    def award(self):
        self.score += 100
    
    def get_score(self):
        return self.score