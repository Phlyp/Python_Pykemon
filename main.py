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

"""
Main menu game loop

*inputs: none
*returns: none
"""
def game_engine():
    while True:
        sys.clear()
        print(f"Hello {player.current_player.name}, what would you like to do?")
        print(" 1. Player Settings \n 2. Edit your team \n 3. Fight!\n 4. Exit!")
        decision = input("Please use the Keys 1-4 + ENTER to choose what to do next! ")
        sys.clear()

        if decision == "1":
            player_settings()
        elif decision == "2":
            team_settings()
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

"""
player settings main menu

*inputs: none
*returns: none
"""
def player_settings():
    while True:
        sys.clear()
        print(f"Hello {player.current_player.name}, what would you like to do?")
        print(" 1. Get player info \n 2. Create new / change player \n 3. Delete all players \n 4. Back to main menu")
        decsision = input("Please use the Keys 1-4 + ENTER to choose what to do next! ")
        sys.clear()

        if decsision == "1":
            player.get_player_info()
            sys.wait_for_keypress()
        elif decsision == "2":
            player.create_new_player()
        elif decsision == "3":
            player.delete_all_players()
            team.delete_all_teams()
        elif decsision == "4":
            print("")
            break
        else:
            print("invalid input given!")
    
"""
team settings main menu

*inputs: none
*outputs: none
"""
def team_settings():
    while True:
        sys.clear()
        print(f"Hello {player.current_player.name}, what would you like to do?")
        print(" 1. Choose your own Team\n 2. Create a random Team \n 3. List Team \n 4. Heal team \n 5. Back to main menu")
        decision = input("Please use the Keys 1-5 + ENTER to choose what to do next! ")
        sys.clear()

        if decision == "1":
            team.delete_team(player.current_player.id)
            team_sel.start_selection(player.current_player.id)
            sys.wait_for_keypress()
        elif decision == "2":
            team.create_random_team(player.current_player.id)
            team.list_team(player.current_player.id)
            sys.wait_for_keypress()
        elif decision == "3":
            team.list_team(player.current_player.id)
            sys.wait_for_keypress()
        elif decision == "4":
            team.heal_team(player.current_player.id)
            print("Healing team!")
            sys.wait_for_keypress()
        elif decision == "5":
            print("")
            break
        else:
            print("invalid input given!")
        print("\n") 


"""
main program funcion
checks if database exists, 
    if not a new player must be created first
    else prompts to select a player
starts main menu loop

"""
if __name__ == "__main__":
    is_new_session = not database.table_exists("team")
    database.initialise()
    sys.clear()
    print("Welcome to Pykemon!\n")

    player.create_new_player()
            

    game_engine()