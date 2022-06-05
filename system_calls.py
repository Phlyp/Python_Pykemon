import os

def clear():
    """
    clear Clears all text from the terminal window to help create a distinction between different game menu screens in the terminal
    differentiates between linux and windows operating systems

    Args: None
    Returns: None

    Test:
        * works on both windows and Linux?
        * call should effectively clear terminal
    """
    if os.name == "nt":
        os.system('cls')
    else:
        os.system('clear')

def wait_for_keypress():
    """
    wait_for_keypress Waits for the user to leave an input, but does not store or return it
    Used to let the user read information before clearing the screen for example when moving to another menu

    Args: None
    Returns: None


    """
    input("press ENTER to continue")

def get_number(question):
    """
    get_number Simple function that asks for a input from the user and checks if that input is a number
    if the given input is a number, it is returned

    Args:
        question (string): Question to use when prompting the user for a numerical input

    Returns:
        int: User input number

    Test:
        * if the user does not give a number, the function should not accept it and ask again
        * return value should be int
    """
    while True:
        try:
            user_input = input(question)
            user_input = int(user_input)
            return user_input
        except:
            print("Invaldid Input!")
