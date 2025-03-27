import random
from email import ReadData 
from player import Player

class GameModel:
    def __init__(self):
        self.player = Player()
        self.emails = ReadData()
        if not self.emails:
            raise Exception("No emails loaded from JSON file!")
        # Create a shuffled order for emails
        self.index_order = list(range(len(self.emails)))
        random.shuffle(self.index_order)
        self.current_index = 0

    def get_current_email(self):
        #Return the current email object or None if we have finished all emails
        if self.current_index < len(self.index_order):
            return self.emails[self.index_order[self.current_index]]
        else:
            return None

    def check_answer(self, answer):
        current_email = self.get_current_email()
        if current_email is None:
            return None, "No email available."
        
        scam_info = current_email.get_scam().lower().strip()
        if answer.upper() == "Y":
            correct = scam_info.startswith("scam")
        elif answer.upper() == "N":
            correct = scam_info.startswith("legit")
        else:
            correct = False

        difficulty = current_email.get_difficulty()
        
        if correct:
            self.player.award(difficulty)  # Award 100 points if correct.
        return correct, current_email.get_explanation()

    def next_email(self):
        self.current_index += 1
        return self.get_current_email()
    
    def get_score(self):
        return self.player.get_score()