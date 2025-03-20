import tkinter as tk
from tkinter import messagebox
from model import GameModel  # Ensure this file is in the same directory and properly implemented

class EmailGameGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Phishing Email Game - GUI")
        self.geometry("600x400")
        
        # Initialize the game model.
        try:
            self.model = GameModel()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.destroy()
            return
        
        self.current_email = None
        
        # Setup the GUI widgets.
        self.create_widgets()
        self.load_current_email()
    
    def create_widgets(self):
        # Score label at the top of the window.
        self.lblScore = tk.Label(self, text=f"Score: {self.model.get_score()}", font=("Arial", 14))
        self.lblScore.pack(pady=10)

        # Frame for displaying email details.
        self.frameEmail = tk.Frame(self)
        self.frameEmail.pack(fill=tk.BOTH, expand=True, padx=10)
        
        self.lblSubject = tk.Label(self.frameEmail, text="", font=("Arial", 16, "bold"), anchor="w")
        self.lblSubject.pack(fill=tk.X, pady=(5,0))
        
        self.lblSender = tk.Label(self.frameEmail, text="", font=("Arial", 14), anchor="w")
        self.lblSender.pack(fill=tk.X, pady=(5,0))
        
        self.lblBody = tk.Label(self.frameEmail, text="", font=("Arial", 12), anchor="w", wraplength=580, justify="left")
        self.lblBody.pack(fill=tk.X, pady=(5,20))
        
        # Frame for the answer buttons.
        self.frameButtons = tk.Frame(self)
        self.frameButtons.pack(pady=10)
        
        self.btnScam = tk.Button(self.frameButtons, text="Scam", width=10, command=self.answer_scam)
        self.btnScam.grid(row=0, column=0, padx=10)
        
        self.btnLegit = tk.Button(self.frameButtons, text="Not Scam", width=10, command=self.answer_legit)
        self.btnLegit.grid(row=0, column=1, padx=10)
        
        # Next Email button.
        self.btnNext = tk.Button(self, text="Next Email", command=self.next_email, state=tk.DISABLED)
        self.btnNext.pack(pady=10)
        
        # Feedback label to show if user's answer is correct or not.
        self.lblFeedback = tk.Label(self, text="", font=("Arial", 12))
        self.lblFeedback.pack(pady=10)
    
    def load_current_email(self):
        """
        Loads the current email from the game model and updates the GUI.
        """
        self.current_email = self.model.get_current_email()
        if self.current_email is None:
            messagebox.showinfo("Game Over", f"Game over! Your final score: {self.model.get_score()}")
            self.quit()
            return
        
        self.lblSubject.config(text=f"Subject: {self.current_email.get_subject()}")
        self.lblSender.config(text=f"Sender: {self.current_email.get_sender()}")
        self.lblBody.config(text=f"Body: {self.current_email.get_body()}")
        self.lblFeedback.config(text="")
        
        # Enable the answer buttons, disable "Next Email" until an answer is given.
        self.btnScam.config(state=tk.NORMAL)
        self.btnLegit.config(state=tk.NORMAL)
        self.btnNext.config(state=tk.DISABLED)
        self.lblScore.config(text=f"Score: {self.model.get_score()}")
    
    def answer_scam(self):
        """Called when the 'Scam' button is pressed."""
        self.process_answer("Y")
    
    def answer_legit(self):
        """Called when the 'Not Scam' button is pressed."""
        self.process_answer("N")
    
    def process_answer(self, answer):
        """
        Uses the game model to check the user's answer.
        Disables the answer buttons after submission and enables the next email button.
        """
        correct, explanation = self.model.check_answer(answer)
        
        # Disable answer buttons.
        self.btnScam.config(state=tk.DISABLED)
        self.btnLegit.config(state=tk.DISABLED)
        
        # Provide feedback.
        if correct:
            self.lblFeedback.config(text="Correct!", fg="green")
        else:
            self.lblFeedback.config(text=f"Incorrect!\nExplanation: {explanation}", fg="red")
        
        # Update the score display.
        self.lblScore.config(text=f"Score: {self.model.get_score()}")
        
        # Enable the Next button so the player can move on.
        self.btnNext.config(state=tk.NORMAL)
    
    def next_email(self):
        """
        Advances to the next email in the model and updates the interface.
        """
        self.model.next_email()
        self.load_current_email()

if __name__ == "__main__":
    app = EmailGameGUI()
    app.mainloop()