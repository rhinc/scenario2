import json
import random
import os
from email import ReadData  # Reads enhanced JSON with id and difficulty

# File to store game progress
PROGRESS_FILE = "progress.json"

def load_progress():
    #Load progress from the progress file, if available.
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, "r") as f:
                data = json.load(f)
                return data
        except Exception as e:
            print("Error loading progress:", e)
    return None

def save_progress(score, asked):
    #save the current score and list of asked email IDs to a progress file
    data = {
        "score": score,
        "asked": asked
    }
    try:
        with open(PROGRESS_FILE, "w") as f:
            json.dump(data, f)
    except Exception as e:
        print("Error saving progress:", e)

def reset_progress():
    #reset progress by deleting the progress file
    if os.path.exists(PROGRESS_FILE):
        os.remove(PROGRESS_FILE)
        print("Progress has been reset.")
    else:
        print("No saved progress found.")

def select_easy_emails(email_objects):
    #Filter emails so that only those marked as easy (using their difficulty field) are returned
    easy_emails = []
    for email in email_objects:
        # If the email has a 'difficulty' attribute, check it; otherwise assume "easy"
        difficulty = getattr(email, 'difficulty', "easy")
        if difficulty.lower() == "easy":
            easy_emails.append(email)
    return easy_emails

def select_medium_emails(email_objects):
    #Filter emails so that only those marked as medium (using their difficulty field) are returned
    medium_emails = []
    for email in email_objects:
        # If the email has a 'difficulty' attribute, check it; otherwise assume "easy"
        difficulty = getattr(email, 'difficulty', "medium")
        if difficulty.lower() == "medium":
            medium_emails.append(email)
    return medium_emails

def select_hard_emails(email_objects):
    #Filter emails so that only those marked as easy (using their difficulty field) are returned
    hard_emails = []
    for email in email_objects:
        # If the email has a 'difficulty' attribute, check it; otherwise assume "easy"
        difficulty = getattr(email, 'difficulty', "hard")
        if difficulty.lower() == "hard":
            hard_emails.append(email)
    return hard_emails

def main():
    print("Welcome to the Phishing Email Game!")
    print("Options: [N]ew Game, [R]esume Game, or type 'reset' to reset progress")
    choice = input("Please choose an option: ").strip().lower()
    
    if choice == "reset":
        reset_progress()
        return  # exit after reset
    elif choice == "r" or choice == "resume":
        progress = load_progress()
        if progress is None:
            print("No saved progress found. Starting a new game.")
            score = 0
            asked = []
        else:
            score = progress.get("score", 0)
            asked = progress.get("asked", [])
            print(f"Resuming game. Current score: {score}")
    elif choice == "n" or choice == "new":
        score = 0
        asked = []
        if os.path.exists(PROGRESS_FILE):
            os.remove(PROGRESS_FILE)
        print("Starting a new game.")
    else:
        print("Invalid choice. Exiting.")
        return

    # load emails from the enhanced JSON (via email.py's ReadData)
    emails = ReadData()
    # Filter for easy emails only
    easy_emails = select_easy_emails(emails)
    medium_emails = select_medium_emails(emails)
    hard_emails = select_hard_emails(emails)
    if not easy_emails and not medium_emails and not hard_emails:
        print("No emails available.")
        return

    # Main game loop: while the player’s score is less than 1500
    while score < 1500:
        if score < 500:
            available_emails = [
                email for email in easy_emails 
                if getattr(email, 'id', None) not in asked
            ]
        elif score < 1000:
            available_emails = [
                email for email in medium_emails 
                if getattr(email, 'id', None) not in asked
            ]
        else:
            available_emails = [
                email for email in hard_emails 
                if getattr(email, 'id', None) not in asked
            ]
        if not available_emails:
            # If all have been asked, allow repetition by resetting the asked list.
            print("All easy emails have been used. Reusing questions.")
            asked = []
            available_emails = easy_emails[:]
        
        email = random.choice(available_emails)
        email_id = getattr(email, 'id', None)

        # Combine subject, sender, and body into one text block (without extra labels)
        content_text = f"{email.get_subject()}\n{email.get_sender()}\n\n{email.get_body()}"
        print("\n--- Email ---")
        print(content_text)
        print("-------------")
        
        user_input = input("Do you think this email is a scam? (Y/N) or type 'reset' to reset progress: ").strip()

        # Allow progress reset at the question prompt.
        if user_input.lower() == "reset":
            reset_progress()
            score = 0
            asked = []
            print("Game progress has been reset. Starting over.")
            continue
        
        # Evaluate answer: Correct answer is determined by the email's scam field.
        scam_field = email.get_scam().lower().strip()
        if user_input.upper() == "Y":
            correct = scam_field.startswith("scam")
        elif user_input.upper() == "N":
            correct = scam_field.startswith("legit")
        else:
            print("Invalid input. No points awarded.")
            correct = False

        if correct:
            score += 100
            print("Correct! You've earned 100 points.")
        else:
            print("Incorrect!")
        print("Explanation:", email.get_explanation())
        print("Your score is now:", score)
        
        # Mark this email as asked (using its unique id if available)
        if email_id is not None:
            asked.append(email_id)
        else:
            asked.append(email.get_subject())
        
        # Save progress after each question
        save_progress(score, asked)
        
        # If the game is not over, ask if the user wants to continue.
        if score < 1500:
            cont = input("Continue? (Y/N): ").strip().lower()
            if cont != "y":
                print("Exiting game. Your progress is saved.")
                return

    print("\nCongratulations! You've reached 1500 points. Game Over.")
    # When finished, progress is cleared.
    if os.path.exists(PROGRESS_FILE):
        os.remove(PROGRESS_FILE)

if __name__ == "__main__":
    main()