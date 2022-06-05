"""Module Description
    * collection of functions to manage the team of a player

    author: Phlyp and hipman8
    date: 05.06.2022
    version: 1.0.0
    license: free
"""

import sqlite3
from database import db_name
import random
import pandas as pd
from playerManager import player_exists

conn = sqlite3.connect(db_name)
cursor = conn.cursor()


def add_pokemon_to_team(player_id, pokemon_id, count):
    """
    add_pokemon_to_team Adds a single pokemon to the team of a player

    Args:
        player_id (int): id of the player whose team the pokemon should be added to
        pokemon_id (int): id of the pokemon being added to the team
        count (int): counts how many pokemon have already been added to the team and saves as pokemon_order in the team table
    
    Returns: None

    Test: 
        * arguments should all be type int
        * player should exist
        * pokemon should exist (0 < pokemon_id < 801)
        * successful execution should add 1 new pokemon to team 
    """
    if type(player_id) != int or type(pokemon_id) != int or type(count) != int:
        print("Error: arguments should all be of type int")
        print("Exiting game")
        exit()
    if player_exists(player_id) == False:
        print("Error: player does not exist")
        print("Exiting game")
        exit()

    cursor.execute("SELECT * FROM pokemon")
    cursor.execute("SELECT name FROM pokemon WHERE pokedex_number = ?", (pokemon_id+1,))
    name = cursor.fetchone()[0]
    print(f'{name} has joined your Team!')
    cursor.execute("SELECT hp FROM pokemon WHERE pokedex_number = ?", (pokemon_id+1,))
    hp = cursor.fetchone()[0]
    cursor.execute("INSERT OR REPLACE INTO team(player_id, pokemon_order, pokedex_number, health, remaining_light, remaining_special) VALUES(?,?,?,?,?,?)", (player_id, count, pokemon_id+1, hp, 8, 6))
    conn.commit()


def create_random_team(player_id):
    """
    create_random_team Creates a random team of 6 Pokemon for a certain player in the player table

    - Deletes old team
    - loop: 
        - picks random pokedex_number, then pulls the data from that pokemon from the pokemon table
        - inserts new pokemon in the team table

    Args:
        player_id (int): id of the player whose team should be randomly created
    
    Returns: None

    Test:
        * player_id should be of type int
        * player should exist
        * successful execution should add 6 new random pokemon to team table  
    """
    if type(player_id) != int:
        print("Error: player_id should be of type int")
        print("Exiting game")
        exit()
    if player_exists(player_id) == False:
        print("Error: player does not exist")
        print("Exiting game")
        exit()

    delete_team(player_id)
    if player_id != 0: print("Creating random Team!")
    cursor.execute("SELECT * FROM pokemon")
    rows = len(cursor.fetchall())

    for i in range(6):
        rand = random.randint(1, rows)
        cursor.execute("SELECT hp FROM pokemon WHERE pokedex_number = ?", (rand,))
        hp = cursor.fetchone()[0]
        cursor.execute("INSERT OR REPLACE INTO team(player_id, pokemon_order, pokedex_number, health, remaining_light, remaining_special) VALUES(?,?,?,?,?,?)", (player_id, i+1, rand, hp, 8, 6))
    conn.commit()

# deletes all teams in the teams database
def delete_all_teams():
    cursor.execute("DELETE FROM team")
    conn.commit()


def delete_team(player_id):
    """
    delete_team Deletes the team of the player

    Args:
        player_id (int): id of the player whose team should be deleted
    
    Returns: None

    Test:
        * player_id should be of type int
        * player should already have a team
        * successful execution should delete team of player_id
    """    
    if type(player_id) != int:
        print("Error: player_id should be of type int")
        print("Exiting game")
        exit()
    if team_size(player_id) == 0:
        print("Error: player does not have a team")
        print("Exiting game")
        exit()

    cursor.execute("DELETE FROM team WHERE player_id = ?", (player_id,))
    conn.commit()


def heal_team(player_id):
    """
    heal_team Heals the entire team of the player specified by player_id

    looks for the default hp of the pokemon in the pokemon table and updates the team table with that value

    Args:
        player_id (int): id of the player whose team should be deleted
    
    Returns: None

    Test:
        * player_id should be of type int
        * player should already have a team
        * successful execution should restore hp for the entire team of player_id
    """
    if type(player_id) != int:
        print("Error: player_id should be of type int")
        print("Exiting game")
        exit()
    if team_size(player_id) == 0:
        print("You have no Team! You can create one by choosing either\n 1. Choose your own Team\n 2. Create a random Team")
        return

    cursor.execute("""UPDATE team
        SET health = (SELECT hp FROM pokemon WHERE pokedex_number = team.pokedex_number)
        WHERE player_id = ?""", (player_id,))
    conn.commit()


def reset_team(player_id):
    """
    reset_team Resets the remaining light and heavy attacks for the pokemon

    Args:
        player_id (int): id of the player whose team should be reset
    
    Returns: None

    Test:
        * player_id should be of type int
        * player should already have a team
        * successful execution should reset remaining_light and remaining_special for the entire team of player_id
    """    
    if type(player_id) != int:
        print("Error: player_id should be of type int")
        print("Exiting game")
        exit()
    if team_size(player_id) == 0:
        print("Error: player does not have a team")
        print("Exiting game")
        exit()

    cursor.execute("""UPDATE team
        SET remaining_light = 8, remaining_special = 6
        WHERE player_id = ?""", (player_id,))
    conn.commit()


def list_team(player_id):
    """
    list_team Lists all the pokemon and their relevant information from the team of the player
    
    If the player does not have a team, does not throw an error, instead informs player that they do not have a team yet

    Args:
        player_id (int): id of the player whose team should be listed
    
    Returns: None

    Test:
        * player_id should be of type int
        * player should already have a team
        * successful execution should list team
    """    
    if type(player_id) != int:
        print("Error: player_id should be of type int")
        print("Exiting game")
        exit()
    if team_size(player_id) == 0:
        print("You have no Team! You can create one by choosing either\n 1. Choose your own Team\n 2. Create a random Team")
        return

    cursor.execute("""SELECT team.pokemon_order, pokemon.name, team.health, pokemon.attack, pokemon.defense, pokemon.type1, pokemon.type2
        FROM team INNER JOIN pokemon 
        ON team.pokedex_number = pokemon.pokedex_number 
        WHERE team.player_id = ?
        ORDER BY team.pokemon_order""", (player_id,))
    team = cursor.fetchall()

    
    print("Your team is currently comprised of: ")
    for row in team:
        if row[6] == None:
            print(f" {row[0]}. {row[1]: <10} hp: {row[2]: <4} attack: {row[3]: <4} defense: {row[4]: <4} type: {row[5]}")
        else:
            print(f" {row[0]}. {row[1]: <10} hp: {row[2]: <4} attack: {row[3]: <4} defense: {row[4]: <4} type: {row[5]} & {row[6]}")


def team_size(player_id):
    """
    team_size Returns the amount of pokemon in the team of the player

    Args:
        player_id (int): id of the player whose team siye should be returned

    Returns:
        int: number of pokemon in the team of the player

    Test:
        * player_id should be of type int
        * player should exist
        * successful execution should return the correct size of the team
    """
    if type(player_id) != int:
        print("Error: player_id should be of type int")
        print("Exiting game")
        exit()
    if player_exists(player_id) == False:
        print("Error: player does not exist")
        print("Exiting game")
        exit()
    
    cursor.execute("SELECT * FROM team WHERE player_id = ?", (player_id,))
    team_size = len(cursor.fetchall())
    return team_size


def alive_team_size(player_id):
    """
    alive_team_size Returns the amount of pokemon still alive in the team of the player

    Args:
        player_id (int): id of the player to count the team size of

    Returns:
        int: size of the team

    Test:
        * player_id should be of type int
        * player should already have a team
        * successful execution should return the correct size of alive pokemon in the team of the player
    """  
    if type(player_id) != int:
        print("Error: player_id should be of type int")
        print("Exiting game")
        exit()
    if team_size(player_id) == 0:
        print("Error: player does not have a team")
        print("Exiting game")
        exit()

    cursor.execute("SELECT * FROM team WHERE player_id = ? AND health > 0", (player_id,))
    team_size = len(cursor.fetchall())
    return team_size