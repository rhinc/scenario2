import random

#make sure textfile is in the same format with no space in between.

#empty list for later use
email_list = []

# declare class
class Email:
    def __init__(self,subject,sender,body,explanation,scam):
        self.subject = subject
        self.sender = sender
        self.body = body
        self.explanation = explanation
        self.scam = scam

    #get methods for data
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

#read data from textfile then store in array(email_list)
def ReadData():
    filename = "email.txt"
    try:
        file = open(filename, "r")
        data = (file.readline()).strip()
        while data != "":
            subject = data
            sender = (file.readline()).strip()
            body = (file.readline()).strip()
            explanation = (file.readline()).strip()
            scam = (file.readline()).strip()
            email_list.append(Email(subject,sender,body,explanation,scam))
            data = (file.readline()).strip()
        file.close()
    except IOError:
        print("Error")
    return email_list


email_list = ReadData()

#create a list for range of email_list
random_list = list(range(len(email_list)))
print(random_list)

#shuffle the list for random selection of email in array and to prevent repetition of emails
random.shuffle(random_list)
for RandomChoice in random_list:
    print(RandomChoice)

    #stores data to be displayed or compared
    subjectdisplay = email_list[RandomChoice].get_subject()
    senderdisplay = email_list[RandomChoice].get_sender()
    bodydisplay = email_list[RandomChoice].get_body()
    explanationdisplay = email_list[RandomChoice].get_explanation()
    scamdisplay = email_list[RandomChoice].get_scam()

    Question = input("Do you think this email is a scam? (Y/N): ")
    if Question == "Y":
        if scamdisplay == "scam":
            print("Correct")
        else:
            print("Incorrect")
            print("Explanation: " + explanationdisplay)
    elif Question == "N":
        if scamdisplay == "legit":
            print("Correct")
        else:
            print("Incorrect")
            print("Explanation: " + explanationdisplay)
    else:
        print("Invalid Input")


    #give player option to continue or end game
    UserInput = input("Do you want to continue? (Y/N): ")
    if UserInput == "N":
        break
    elif UserInput == "Y":
        continue
    else:
        print("Invalid Input")

print("End of Program")