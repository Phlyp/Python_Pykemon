import os
import string
from sys import meta_path
import sqlite3 as sdb
import pandas as pd
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()

db_name = os.path.join("Data","db.sqlite")

sqlite_conn = sdb.connect(db_name)
sqlite_cursor = sqlite_conn.cursor()

"""
initialises and resets the database

*inputs: none
*outputs: none
"""
def initialise():

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
    
"""
checks if a table exists in the database

*inputs: 
    name: name of the table to check
*outputs:
    boolean: True or False depending on the table existing
"""
def table_exists(name):
    sqlite_cursor.execute(''' SELECT COUNT(name) FROM sqlite_master WHERE type='table' AND name=? ''', (name,))
    if sqlite_cursor.fetchone()[0]==1:
        return True 
    else:
        return False


