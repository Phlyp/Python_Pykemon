"""Module Description
    * Functions that define the main menus of the Pykemon game

    author: Phlyp, hipman8 and Novadgaf
    date: 05.06.2022
    version: 1.0.0
    license: free
"""

import os
import system_calls as sys

import database
import teamManager as team
import fightManager as fight
import teamSelection as team_sel
import playerManager as player

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame

clear = lambda: os.system('cls')


def game_engine():
    """
    game_engine Main menu game loop

    This Loop functions as the main menu for the app, allowing the player to choose which sub-functionality to execute next

    Args: None
    
    Returns: None

    Test:
        * test inputs 1-4 and their expected outcomes
        * other inputs should not be accepted
    """                
    while True:
        sys.clear()
        print(f"Hello {player.current_player.name}, what would you like to do?")
        print(" 1. Player Settings \n 2. Edit your team \n 3. Fight!\n 4. Exit!")
        decision = input("Please use the Keys 1-4 + ENTER to choose what to do next! ")
        sys.clear()

        if decision == "1":
            player.player_settings()
        elif decision == "2":
            team.team_settings(player.current_player.id)
        elif decision == "3":
            if team.team_size(player.current_player.id) == 0:
                print("You must first create your team!")
                print("To create your team go to 'Edit Your Team' in the main Menu!")
                sys.wait_for_keypress()
            else:
                fight.fight_engine()
        elif decision == "4":
            print("Goodbye!")
            quit()
        else:
            print("invalid input given!")


if __name__ == "__main__":
    # main program funcion initiatlises Database
    is_new_session = not database.table_exists("team")
    database.initialise()
    sys.clear()
    print("Welcome to Pykemon!\n")

    player.player_selection()
            
    # starts the main menu game loop
    game_engine()