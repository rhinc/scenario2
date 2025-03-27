class Player:
    def __init__(self):
        self.score = 0

    def award(self,difficulty):
        if difficulty == "easy":
            self.score += 50
        elif difficulty == "medium":
            self.score += 100
        else:
            self.score += 150
    
    def get_score(self):
        return self.score