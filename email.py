import json
import random

# Empty list for storing email objects
email_list = []

# Declare the Email class
class Email:
    def __init__(self, subject, sender, body, explanation, scam):
        self.subject = subject
        self.sender = sender
        self.body = body
        self.explanation = explanation
        self.scam = scam

    # Getter methods for data
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

def ReadData():
    """
    Reads email data from a JSON file ('email.json') that contains a list of dictionaries.
    Each dictionary should have keys: "subject", "sender", "body", "explanation", "scam".
    The 'scam' key is expected to be a boolean (true means scam, false means legit).
    For compatibility with our answer-checking logic (which expects a string starting with "scam" or "legit"),
    we convert the boolean value accordingly.
    """
    filename = "email.json"
    try:
        with open(filename, "r") as file:
            data = json.load(file)
            for entry in data:
                subject = entry.get("subject", "")
                sender = entry.get("sender", "")
                body = entry.get("body", "")
                explanation = entry.get("explanation", "")
                # Convert boolean to string: "scam" if true, "legit" if false.
                is_scam = entry.get("scam", True)
                scam = "scam" if is_scam else "legit"
                email_list.append(Email(subject, sender, body, explanation, scam))
    except IOError as e:
        print("Error reading JSON file:", e)
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
    return email_list

# Load emails from JSON
email_list = ReadData()

# Create a list for random order of email indexes to prevent repetition
random_indexes = list(range(len(email_list)))
random.shuffle(random_indexes)

# (Optional debug printing removed for production use)