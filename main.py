from model import GameModel

def main():
    # Create a game model instance.
    model = GameModel()
    
    while True:
        current_email = model.get_current_email()
        if current_email is None:
            break
        
        # Display the email details
        print("\n--------------------------------")
        print(f"Subject: {current_email.get_subject()}")
        print(f"Sender: {current_email.get_sender()}")
        print(f"Body: {current_email.get_body()}\n")
        print("Do you think this email is a scam?")
        
        # Get user's answer input.
        answer = input("Enter Y for scam, N for legit: ").strip().upper()
        correct, explanation = model.check_answer(answer)
        if correct is None:
            print("No email to evaluate.")
            break
            
        if correct:
            print("Correct!")
        else:
            print("Incorrect.")
        print("Explanation:", explanation)
        print("Current Score:", model.get_score())
        
        # Ask if the user wants to continue.
        cont = input("Continue to next email? (Y/N): ").strip().upper()
        if cont == "N":
            break
        
        model.next_email()
    
    print("\nGame Over!")
    print("Your final score is:", model.get_score())

if __name__ == "__main__":
    main()