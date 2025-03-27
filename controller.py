import json
import os

# File to store game progress
PROGRESS_FILE = "progress.json"

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, "r") as f:
                data = json.load(f)
                return data
        except Exception as e:
            print("Error loading progress:", e)
    return None

def save_progress(score, asked, current_difficulty):
    data = {
        "score": score,
        "asked": asked,
        "difficulty": current_difficulty
    }
    try:
        with open(PROGRESS_FILE, "w") as f:
            json.dump(data, f)
    except Exception as e:
        print("Error saving progress:", e)

def reset_progress():
    if os.path.exists(PROGRESS_FILE):
        os.remove(PROGRESS_FILE)
        print("Progress has been reset.")
    else:
        print("No saved progress found.")

def select_emails_by_difficulty(email_objects, difficulty):
    selected = []
    for email in email_objects:
        if getattr(email, 'difficulty', "easy").lower() == difficulty.lower():
            selected.append(email)
    return selected