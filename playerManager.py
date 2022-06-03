from database import db_name
import sqlite3

conn = sqlite3.connect(db_name)
cursor = conn.cursor()
start_dollars = 1000

"""
(abstract) class that saves the id and name of the current player for convenience
"""
class current_player:
    id = 1
    name = ""

"""
creates a new player
asks user for a name input, then adds player to players table and initialises base values

*inputs: none
*outputs: none
"""
def create_new_player():
    name = input("Please enter a name for your new player: ")

    cursor.execute("SELECT COUNT(*) FROM players WHERE name = ?", (name,))
    while cursor.fetchone()[0] > 0:
        name = input("Name already exists! Please enter a new name: ")
        cursor.execute("SELECT COUNT(*) FROM players WHERE name = ?", (name,))

    cursor.execute("INSERT INTO players(name, is_bot, xp, level, dollars, high_score) VALUES(?,0,0,0,?,0)", (name, start_dollars))
    conn.commit()
    player_id = cursor.execute("SELECT player_id FROM players WHERE name = ?", (name,)).fetchone()[0]
    current_player.id = player_id
    current_player.name = cursor.execute("SELECT name FROM players WHERE player_id = ?", (player_id,)).fetchone()[0]

"""
prints all existing players
allows user to choose a player from list

*inputs: none
*outputs: none
"""
def change_current_player():
    cursor.execute("SELECT COUNT(*) FROM players WHERE is_bot = 0")
    total_rows = cursor.fetchone()[0]
    print("These are the current players:")
    cursor.execute("SELECT player_id,name,xp,level,dollars,high_score FROM players WHERE is_bot = 0")
    players = cursor.fetchall()
    for row in players:
        print(f" {row[0]}. Name: {row[1]}, Xp: {row[2]}, Level: {row[3]}, Dollars: {row[4]}, High Score: {row[5]}")

    id = int(input(f"Please use the Keys 1-{total_rows} + ENTER to select your player: " ))
    cursor.execute("SELECT COUNT(*) FROM players WHERE player_id = ?", (id,))
    while cursor.fetchone()[0] == 0:
        print("Error: Player does not exist!")
        id = int(input(f"Please use the Keys 1-{total_rows} + ENTER to select your player: "))
        cursor.execute("SELECT COUNT(*) FROM players WHERE player_id = ?", (id,))

    current_player.id = id
    current_player.name = cursor.execute("SELECT name FROM players WHERE player_id = ?", (id,)).fetchone()[0]
    print("Hello %s!"%current_player.name)

"""
returns basic information on the current player

*inputs: none
*outputs: none
"""
def get_player_info():
    info = cursor.execute("SELECT player_id,name,xp,level,dollars,high_score FROM players WHERE player_id = ?", (current_player.id,)).fetchone()
    print(f" {info[0]}. Name: {info[1]}, Xp: {info[2]}, Level: {info[3]}, Dollars: {info[4]}, High Score: {info[5]}")

"""
deletes all players in the players table 

*inputs: none
*outputs: none
"""
def delete_all_players():
    cursor.execute("DELETE FROM players WHERE is_bot = 0")
    conn.commit()
    create_new_player()