import os

def clear():
    if os.name == "nt":
        os.system('cls')
    else:
        os.system('clear')

def wait_for_keypress():
    input("press ENTER to continue")

def get_number(question):
    while True:
        try:
            user_input = input(question)
            user_input = int(user_input)
            return user_input
        except:
            print("Invaldid Input!")
