import tkinter as tk
from tkinter import messagebox
import random
from player import Player
from email import ReadData  # Ensure this is the correct module name for your email code

class EmailGameView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Phishing Email Game")
        self.geometry("600x400")
        
        # instantiate player and load emails
        self.player = Player()
        self.emails = ReadData()
        if not self.emails:
            messagebox.showerror("Error", "No emails loaded!")
            self.destroy()
        
        # Shuffle email indexes for random order
        self.random_indexes = list(range(len(self.emails)))
        random.shuffle(self.random_indexes)
        self.current_index = 0  # pointer in the shuffled list
        
        # Create the UI components
        self.create_widgets()
        self.load_email()

    def create_widgets(self):
        # Display current score in a label
        self.score_label = tk.Label(self, text=f"Score: {self.player.get_score()}", font=("Helvetica", 12))
        self.score_label.pack(pady=10)
        
        # Frame for email details (subject, sender, body)
        self.email_frame = tk.Frame(self)
        self.email_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.subject_label = tk.Label(self.email_frame, text="Subject: ", anchor="w", font=("Helvetica", 14, "bold"))
        self.subject_label.pack(fill=tk.X)
        
        self.sender_label = tk.Label(self.email_frame, text="Sender: ", anchor="w", font=("Helvetica", 12))
        self.sender_label.pack(fill=tk.X)
        
        self.body_label = tk.Label(self.email_frame, text="Body: ", anchor="w", wraplength=550, font=("Helvetica", 12))
        self.body_label.pack(fill=tk.X, pady=5)
        
        # Label for feedback (Correct / Incorrect)
        self.feedback_label = tk.Label(self, text="", font=("Helvetica", 12))
        self.feedback_label.pack(pady=5)
        
        # Frame for the Answer buttons
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(pady=10)
        
        self.scam_button = tk.Button(
            self.button_frame,
            text="Scam", 
            width=10,
            command=lambda: self.check_answer("Y")
        )
        self.scam_button.grid(row=0, column=0, padx=10)
        
        self.legit_button = tk.Button(
            self.button_frame,
            text="Not Scam", 
            width=10,
            command=lambda: self.check_answer("N")
        )
        self.legit_button.grid(row=0, column=1, padx=10)
        
        # Frame for navigation (Next, Quit)
        self.navigation_frame = tk.Frame(self)
        self.navigation_frame.pack(pady=10)

        self.next_button = tk.Button(
            self.navigation_frame,
            text="Next Email",
            command=self.next_email,
            state=tk.DISABLED
        )
        self.next_button.grid(row=0, column=0, padx=10)
        
        self.quit_button = tk.Button(
            self.navigation_frame,
            text="Quit",
            command=self.quit
        )
        self.quit_button.grid(row=0, column=1, padx=10)
    
    def load_email(self):
        """
        Loads the current email (using a shuffled order) and updates the
        labels to display the email's subject, sender, and body.
        """
        if self.current_index < len(self.random_indexes):
            email_obj = self.emails[self.random_indexes[self.current_index]]
            self.current_email = email_obj  # store the current email object
            
            self.subject_label.config(text=f"Subject: {email_obj.get_subject()}")
            self.sender_label.config(text=f"Sender: {email_obj.get_sender()}")
            self.body_label.config(text=f"Body: {email_obj.get_body()}")
            self.feedback_label.config(text="")
            
            # Enable the answer buttons for a fresh email
            self.scam_button.config(state=tk.NORMAL)
            self.legit_button.config(state=tk.NORMAL)
            self.next_button.config(state=tk.DISABLED)
        else:
            self.end_game()
    
    def check_answer(self, user_input):
        """
        Compares the user's answer with the email data. If the user clicks "Scam"
        (i.e. user_input == "Y"), the email's scam value should be "scam" (or begin with "scam").
        If the user clicks "Not Scam" (i.e. user_input == "N"), the value should be "legit" (or
        begin with "legit"). Updates the score if the answer is correct.
        """
        # Obtain the scam field and convert to lowercase for flexible matching
        scam_value = self.current_email.get_scam().lower().strip()
        correct = False

        if user_input == "Y":
            # Check if the email is marked as a scam
            correct = scam_value == "scam" or scam_value.startswith("scam")
        elif user_input == "N":
            # Check if the email is marked as legit
            correct = scam_value == "legit" or scam_value.startswith("legit")
        
        if correct:
            self.player.award()  # Award 100 points
            self.score_label.config(text=f"Score: {self.player.get_score()}")
            self.feedback_label.config(text="Correct!", fg="green")
        else:
            explanation = self.current_email.get_explanation()
            self.feedback_label.config(text=f"Incorrect. Explanation: {explanation}", fg="red")
        
        # Disable answer buttons until the next email is loaded
        self.scam_button.config(state=tk.DISABLED)
        self.legit_button.config(state=tk.DISABLED)
        self.next_button.config(state=tk.NORMAL)
    
    def next_email(self):
        """
        Moves on to the next email by incrementing the index and loading
        the email. If no more emails remain, the game ends.
        """
        self.current_index += 1
        self.load_email()
    
    def end_game(self):
        """
        Ends the game by showing a "Game Over" message with the final score,
        and then closes the window.
        """
        messagebox.showinfo("Game Over", f"Game over! Your final score: {self.player.get_score()}")
        self.destroy()

if __name__ == "__main__":
    app = EmailGameView()
    app.mainloop()