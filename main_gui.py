import tkinter as tk
from tkinter import messagebox
import random
import controller  # Uses controller functions for progress and filtering
from model import GameModel  # GameModel loads emails from email.json via ReadData

class EmailGameGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MailMaster Game")
        self.minsize(1200, 600)  # Allow window resizing with a minimum size

        #initialise progress variables:
        self.config_choice = None
        self.asked = []

        #show configuration dialog before initialising game
        self.config_dialog()
        if self.config_choice == "reset":
            controller.reset_progress()
            self.config_choice = "new"

        #instantiate the game model
        try:
            self.model = GameModel()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.destroy()
            return

        # if resuming, attempt to load saved progress
        if self.config_choice == "resume":
            progress = controller.load_progress()
            if progress is not None:
                saved_score = progress.get("score", 0)
                self.model.player.score = saved_score
                self.asked = progress.get("asked", [])
                messagebox.showinfo("Resuming Game", f"Your current score is {saved_score}.")
            else:
                messagebox.showinfo("Info", "No saved progress found. Starting a new game.")
                self.model.player.score = 0
                self.asked = []
        else:
            self.model.player.score = 0
            self.asked = []
            controller.reset_progress()

        #retrieve the complete email list from the model
        self.all_emails = self.model.emails
        
        #use controller functions to filter emails by difficulty
        self.easy_emails   = controller.select_easy_emails(self.all_emails)
        self.medium_emails = controller.select_medium_emails(self.all_emails)
        self.hard_emails   = controller.select_hard_emails(self.all_emails)

        #build UI components
        self.create_widgets()
        self.load_current_email()

    def config_dialog(self):
        dialog = tk.Toplevel(self)
        dialog.title("Game Configuration")
        dialog.grab_set()  # make the dialog modal
        
        tk.Label(dialog, text="Select an option:").pack(pady=10)

        def set_new():
            self.config_choice = "new"
            dialog.destroy()

        def set_resume():
            self.config_choice = "resume"
            dialog.destroy()

        def set_reset():
            self.config_choice = "reset"
            dialog.destroy()

        tk.Button(dialog, text="New Game", width=20, command=set_new).pack(pady=5)
        tk.Button(dialog, text="Resume Game", width=20, command=set_resume).pack(pady=5)
        tk.Button(dialog, text="Reset Progress", width=20, command=set_reset).pack(pady=5)
        self.wait_window(dialog)

    def create_widgets(self):
        # Row 0: Score label
        self.lblScore = tk.Label(self, text=f"Score: {self.model.get_score()}", font=("Arial", 14))
        self.lblScore.grid(row=0, column=0, pady=10)

        # Row 1: Email content (subject, sender, and body combined, no extra labels)
        self.lblContent = tk.Message(self, text="", font=("Arial", 12), width=580)
        self.lblContent.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Row 2: Feedback text (to show the explanation after answer evaluation)
        self.lblFeedback = tk.Message(self, text="", font=("Arial", 12), width=580)
        self.lblFeedback.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        # Row 3: Dynamic button row (Answer buttons or Next Email button)
        self.frameAnswer = tk.Frame(self)
        self.frameAnswer.grid(row=3, column=0, pady=5)

        # Answer buttons
        self.btnScam = tk.Button(
            self.frameAnswer, text="Scam", width=12, 
            command=lambda: self.process_answer("Y")
        )
        self.btnNotScam = tk.Button(
            self.frameAnswer, text="Not Scam", width=12,
            command=lambda: self.process_answer("N")
        )
        self.btnScam.grid(row=0, column=0, padx=5)
        self.btnNotScam.grid(row=0, column=1, padx=5)

        # Next Email button (hidden until an answer is processed)
        self.btnNext = tk.Button(
            self.frameAnswer, text="Next Email", width=12, command=self.next_email
        )

        # Row 4: Quit Game button row
        self.frameQuit = tk.Frame(self)
        self.frameQuit.grid(row=4, column=0, pady=10)
        self.btnQuit = tk.Button(
            self.frameQuit, text="Quit Game", width=12, command=self.quit
        )
        self.btnQuit.pack()

        # Configure grid resizing behavior
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def load_current_email(self):
        if self.model.get_score() >= 1500:
            messagebox.showinfo("Game Over", f"Game over! Your final score is {self.model.get_score()}")
            controller.reset_progress()
            self.destroy()
            return

        score = self.model.get_score()
        if score < 500:
            available_emails = [
                email for email in self.easy_emails 
                if getattr(email, "id", email.get_subject()) not in self.asked
            ]
        elif score < 1000:
            available_emails = [
                email for email in self.medium_emails 
                if getattr(email, "id", email.get_subject()) not in self.asked
            ]
        else:
            available_emails = [
                email for email in self.hard_emails 
                if getattr(email, "id", email.get_subject()) not in self.asked
            ]
        if not available_emails:
            # if all emails for the current difficulty have been used, reset the asked list
            self.asked = []
            if score < 500:
                available_emails = self.easy_emails[:]
            elif score < 1000:
                available_emails = self.medium_emails[:]
            else:
                available_emails = self.hard_emails[:]

        self.current_email = random.choice(available_emails)
        content_text = (
            f"{self.current_email.get_subject()}\n"
            f"{self.current_email.get_sender()}\n\n"
            f"{self.current_email.get_body()}"
        )
        self.lblContent.config(text=content_text)
        self.lblFeedback.config(text="")
        self.btnScam.grid()
        self.btnNotScam.grid()
        self.btnNext.grid_remove()
        self.lblScore.config(text=f"Score: {self.model.get_score()}")

    def process_answer(self, answer):
        correct, explanation = self.model.check_answer(answer)
        if correct:
            feedback_text = f"Correct!\nExplanation: {explanation}"
            self.lblFeedback.config(fg="green")
        else:
            feedback_text = f"Incorrect!\nExplanation: {explanation}"
            self.lblFeedback.config(fg="red")
        self.lblFeedback.config(text=feedback_text)
        self.lblScore.config(text=f"Score: {self.model.get_score()}")

        #record that this email has been asked. Use its unique id if available
        key = getattr(self.current_email, "id", self.current_email.get_subject())
        self.asked.append(key)

        #save progress using the controller
        controller.save_progress(self.model.get_score(), self.asked)

        #hide answer buttons and show the Next Email button
        self.btnScam.grid_remove()
        self.btnNotScam.grid_remove()
        self.btnNext.grid(row=0, column=0, padx=5)

    def next_email(self):
        self.model.next_email()  # Advance model state if needed.
        self.load_current_email()

if __name__ == "__main__":
    app = EmailGameGUI()
    app.mainloop()