class Email:
    def __init__(self,subject,sender,body,explanation,scam):
        self.subject = subject
        self.sender = sender
        self.body = body
        self.explanation = explanation
        self.scam = scam

    def give_explanation(self):
        return self.explanation

    def get_answer(self,Player,guess):
        if guess == self.scam:
            Player.award()
        self.give_explanation()