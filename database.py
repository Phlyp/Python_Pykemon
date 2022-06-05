"""Module Description
    * module to initialise and get general information about the entire database used for storing data in this app

    author: Phlyp
    date: 05.06.2022
    version: 1.0.0
    license: free
"""

import os
import sqlite3 as sdb
import pandas as pd


db_name = os.path.join("Data","db.sqlite")

sqlite_conn = sdb.connect(db_name)
sqlite_cursor = sqlite_conn.cursor()


def initialise():
    """
    initialise initialises and resets the database

    This function is called each time when the app is started

    Args: None

    Returns: None

    Test: 
        * successful exectution should lead to database with the tables [pokemon, attacks, players, team]
    """    
    pokemon_data = pd.read_csv("Data/pokemon.csv", encoding='utf8')
    pokemon_data.to_sql("pokemon", sqlite_conn, index=False, if_exists="replace")

    pokemon_attacks = pd.read_csv("Data/attacks.csv")
    pokemon_attacks.to_sql("attacks", sqlite_conn, index=False, if_exists="replace")

    sqlite_cursor.execute("""CREATE TABLE IF NOT EXISTS players(
        player_id INTEGER PRIMARY KEY,
        name VARCHAR(255) NOT NULL UNIQUE,
        is_bot INTEGER,
        xp INTEGER,
        level INTEGER,
        dollars INTEGER,
        high_score INTEGER,
        CHECK(is_bot IN (0,1)))""")

    sqlite_cursor.execute("""CREATE TABLE IF NOT EXISTS team(
        team_id INTEGER PRIMARY KEY,
        player_id INTEGER,
        pokemon_order INTEGER,
        pokedex_number INTEGER,
        health INTEGER,
        remaining_light INTEGER,
        remaining_special INTEGER,
        FOREIGN KEY (player_id) REFERENCES players(player_id))""")
    
    sqlite_cursor.execute("INSERT OR REPLACE INTO players VALUES(0, 'bot', 1, 0, 0, 0, 0)")
    sqlite_conn.commit()
    
def table_exists(name):
    """
    table_exists Checks if a table exists in the database

    Args:
        name (string): Name of the table whose existence should be checked

    Returns:
        boolean: True if the table exists, False otherwise

    Test:
        * name should be of type string
        * should correctly recognize if table exists or not
    """
    if type(name) != str:
        print("Error: parameter should be of type string!")
        print("Exiting game")
        exit()

    sqlite_cursor.execute(''' SELECT COUNT(name) FROM sqlite_master WHERE type='table' AND name=? ''', (name,))
    if sqlite_cursor.fetchone()[0]==1:
        return True 
    else:
        return False


