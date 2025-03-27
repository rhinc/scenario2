import json
import random

# Empty list for storing email objects
email_list = []

# Declare the Email class with difficulty
class Email:
    def __init__(self, subject, sender, body, explanation, scam, difficulty="easy"):
        self.subject = subject
        self.sender = sender
        self.body = body
        self.explanation = explanation
        self.scam = scam
        self.difficulty = difficulty  

    #getter methods for data
    def get_subject(self):
        return self.subject
    
    def get_sender(self):
        return self.sender
    
    def get_body(self):
        return self.body
    
    def get_explanation(self):
        return self.explanation

    def get_scam(self):
        return self.scam
    
    def get_difficulty(self):
        return self.difficulty

def ReadData():
    filename = "email.json"
    try:
        with open(filename, "r") as file:
            data = json.load(file)
            for entry in data:
                subject = entry.get("subject", "")
                sender = entry.get("sender", "")
                body = entry.get("body", "")
                explanation = entry.get("explanation", "")
                is_scam = entry.get("scam", True)
                scam = "scam" if is_scam else "legit"
                difficulty = entry.get("difficulty", "") 
                email_list.append(Email(subject, sender, body, explanation, scam, difficulty))
    except IOError as e:
        print("Error reading JSON file:", e)
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
    return email_list