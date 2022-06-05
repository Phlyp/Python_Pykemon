"""Module Description
    * module that enables a fight between two pokemon, the player and the bot
    * includes a class to manage an actively fighting pokemon
    * includes functions to execute all essential actions when in a pokemon fight 

    author: Phlyp, Novadgaf and hipman8
    date: 05.06.2022
    version: 1.0.0
    license: free
"""

from tokenize import Special
import system_calls as sys
import sqlite3
import random
from database import db_name
from playerManager import current_player
import teamManager
import logging

logger = logging.getLogger("fight")

conn = sqlite3.connect(db_name)
cursor = conn.cursor()


class pokemon:
    """
    Class to save some basic information on a pokemon for convenience
    Saves the team_id, name and pokedex_number of the pokemon
    Contains a method to get and set the hp of the pokemon
    """
    # class variables
    team_id = 0
    name = ""
    pokedex_number = 0

    # constructor
    def __init__(self):
        pass

    # class functions
    def get_hp(self):
        """
        get_hp Returns the hp of the pokemon in the team table

        Args: None

        Returns:
            int: health of the pokemon
        """
        logger.info(f"getting hp of pokemon {self.team_id}")
        return cursor.execute("SELECT health FROM team WHERE team_id = ?", (self.team_id,)).fetchone()[0]
    

    def set_hp(self, new_hp):
        """
        set_hp Sets the hp of the pokemon in the team table

        Args:
            new_hp (int): new hp to set the hp in the table of the pokemon
        
        Returns: None

        Test:
            * new_hp should be of type int
            * successful execution should edit hp for the pokemon in the team table 
        """
        if type(new_hp) != int:
            print("Error: parameter should be of type int!")
            print("Exiting game")
            logger.error("parameter is not of type int")
            exit()
        logger.info(f"setting hp of pokemon {self.team_id} to {new_hp}")
        cursor.execute("UPDATE team SET health = ? WHERE team_id = ?", (new_hp, self.team_id))
        conn.commit()

# initialise pokemon classes
player_pokemon = pokemon()
bot_pokemon = pokemon()


def choose_pokemon():
    """
    choose_pokemon Prompts the user to choose a pokemon from his team

    - Starts by listing all available pokemon
    - Based on input changes the values of the player_pokemon object
    - Only works for the actual player!

    Args: None

    Returns: None

    Test:
        * successful execution should save all relevent data of the chosen pokemon in the player_pokemon class
        * player input should be between 1-6
        * pokemon cannot have already fainted
    """
    logger.info("choosing pokemon")    
    teamManager.list_team(current_player.id)

    team_size = teamManager.team_size(current_player.id)

    decision = sys.get_number(f"Please use the Keys 1-{team_size} + ENTER to choose which pokemon to send into battle! ")
    while decision < 1 or decision > team_size:
        logger.warning("invalid input given")
        print("Invalid input given!")
        decision = int(input(f"Please use the Keys 1-{team_size} + ENTER to choose which pokemon to send into battle! "))
    player_pokemon.team_id = cursor.execute("SELECT team_id FROM team WHERE player_id = ? AND pokemon_order = ?", (current_player.id, decision)).fetchone()[0]
    hp = cursor.execute("SELECT health FROM team WHERE team_id = ?", (player_pokemon.team_id,)).fetchone()[0]
    if hp < 1:
        sys.clear()
        logger.warning("You can't choose a pokemon who has already fainted!")
        print("You can't choose a pokemon who has already fainted!")
        choose_pokemon()
        return
    logger.info(f"selecting pokemon {player_pokemon.team_id}")
    cursor.execute("""SELECT pokemon.name FROM team
        INNER JOIN pokemon ON team.pokedex_number = pokemon.pokedex_number 
        WHERE team.team_id = ?""", (player_pokemon.team_id,))
    player_pokemon.name = cursor.fetchone()[0]

    cursor.execute("""SELECT pokemon.pokedex_number FROM team
        INNER JOIN pokemon ON team.pokedex_number = pokemon.pokedex_number 
        WHERE team.team_id = ?""", (player_pokemon.team_id,))
    player_pokemon.pokedex_number = cursor.fetchone()[0]


def choose_bot_pokemon():
    """
    choose_bot_pokemon Randomly chooses a pokemon for the bot player

    changes the values saved in the bot_pokemon object 

    Args: None

    Returns: None

    Test:
        * successful execution should save all relevent data of the chosen pokemon in the bot_pokemon class
        * chosen pokemon should have positive hp (cannot already have fainted)
    """
    logger.info("choosing bot pokemon")    
    alive_pokemon = cursor.execute("SELECT team_id FROM team WHERE player_id = 0 AND health > 0").fetchall()
    bot_pokemon.team_id = random.choice(alive_pokemon)[0]
    logger.info(f"bot chose pokemon {bot_pokemon.team_id}")
    cursor.execute("""SELECT pokemon.name FROM 
        team INNER JOIN pokemon ON team.pokedex_number = pokemon.pokedex_number 
        WHERE team.team_id = ?""", (bot_pokemon.team_id,))
    bot_pokemon.name = cursor.fetchone()[0]
    cursor.execute("""SELECT pokemon.pokedex_number FROM team
        INNER JOIN pokemon ON team.pokedex_number = pokemon.pokedex_number 
        WHERE team.team_id = ?""", (bot_pokemon.team_id,))
    bot_pokemon.pokedex_number = cursor.fetchone()[0]


def choose_attack():
    """
    choose_attack Prompts the user to choose an attack

    - Starts by getting all available attacks for the player_pokemon
    - Lists all attacks and waits for input
    - Checks if there are enough attacks remaining
    - Calls the attack function
    - Only works for the player!

    Args: None

    Returns:
        int: (0 or 1) returns a 1 if the user chooses to abort the attack process, and a 0 when an attack is completed 

    Test:
        * should have different options based on the type of the pokemon
        * inputs other than 1-3/4 should not be accepted
        * should correctly execute attack function and return 1 if attack is chosen
    """
    logger.info("choosing attack")    
    pokedex_number = player_pokemon.pokedex_number
    (total_light, total_special) = (8,6)
    basic_attack = "Tackle"

    type0 = "basic"
    (type1, type2) = cursor.execute("SELECT type1, type2 FROM pokemon WHERE pokedex_number = ?", (player_pokemon.pokedex_number,)).fetchone()

    remaining_light = cursor.execute("SELECT remaining_light FROM team WHERE team_id = ?", (player_pokemon.team_id,)).fetchone()[0]
    remaining_special = cursor.execute("SELECT remaining_special FROM team WHERE team_id = ?", (player_pokemon.team_id,)).fetchone()[0]

    sp_attack1 = cursor.execute("SELECT Attack FROM attacks WHERE Type = ?", (type1,)).fetchone()[0]
    # because some pokemon have 1, and some pokemon have 2 types, we need to differentiate when listing the attacks and asking for an input
    if type2 is not None:
        sp_attack2 = cursor.execute("SELECT Attack FROM attacks WHERE Type = ?", (type2,)).fetchone()[0]

        sys.clear()
        print("It's your turn!")
        print(f"You: {player_pokemon.name: <10} hp: {player_pokemon.get_hp(): <10} Enemy: {bot_pokemon.name: <10} hp: {bot_pokemon.get_hp()}")
        print(f" 1. {basic_attack: <13} type: {type0: <10} remaining: {remaining_light}/{total_light}")
        print(f" 2. {sp_attack1: <13} type: {type1: <10} remaining: {remaining_special}/{total_special}")
        print(f" 3. {sp_attack2: <13} type: {type2: <10} remaining: {remaining_special}/{total_special}")
        print(" 4. Go back")

        while True:
            decision = input("Please use the Keys 1-4 + ENTER to choose your attack! ")
            if decision == "1":
                if remaining_light < 0:
                    print("No basic attacks remaining!")
                    continue
                attack(basic_attack, type0, player_pokemon, bot_pokemon)
                break
            elif decision == "2":
                if remaining_special < 0:
                    print("No special attacks remaining!")
                    continue
                attack(sp_attack1, type1, player_pokemon, bot_pokemon)
                break
            elif decision == "3":
                if remaining_special < 0:
                    print("No special attacks remaining!")
                    continue
                attack(sp_attack2, type2, player_pokemon, bot_pokemon)
                break
            elif decision == "4":
                return 1
            else:
                logger.warning("invalid input")
                print("Invalid Input given!")
    else:
        sys.clear()
        print("It's your turn!")
        print(f"You: {player_pokemon.name: <10} hp: {player_pokemon.get_hp(): <10} Enemy: {bot_pokemon.name: <10} hp: {bot_pokemon.get_hp()}")
        print(f" 1. {basic_attack: <13} type: {type0: <10} remaining: {remaining_light}/{total_light}")
        print(f" 2. {sp_attack1: <13} type: {type1: <10} remaining: {remaining_special}/{total_special}")
        print(" 3. Go back")
        decision = ""

        while True:
            decision = input("Please use the Keys 1-3 + ENTER to choose your attack! ")
            if decision == "1":
                if remaining_light < 0:
                    print("No basic attacks remaining!")
                    continue
                attack(basic_attack, type0, player_pokemon, bot_pokemon)
                break
            elif decision == "2":
                if remaining_special < 0:
                    print("No special attacks remaining!")
                    continue
                attack(sp_attack1, type1, player_pokemon, bot_pokemon)
                break
            elif decision == "3":
                return 1
            else:
                logger.warning("invalid input")
                print("Invalid Input given!")
    return 0
        

def attack(attack_name, type, attacking_pokemon: pokemon, defending_pokemon: pokemon):
    """
    attack Performs an attack and inflicts damage on the defending pokemon
        
    - First decrements remaining attack column (light/special)
    - Then calculates damage based on simplified version of this formula https://bulbapedia.bulbagarden.net/wiki/Damage
    - Checks if defending_pokemon fainted (hp < 0)
        - if so, calls checkWin() function
        - then calls choose_pokemon or choose_bot_pokemon depending on who the defender was

    Args:
        attack_name (string): name of the attack used
        type (string): type of the attack used
        attacking_pokemon (pokemon): pokemon object for the pokemon using the attack
        defending_pokemon (pokemon): pokemon object for the pokemon receiving the attack
    
    Returns: None

    Test:
        * are attack_name and type of type string?
        * damage is successfully calculated
        * defending pokemon has correct amount of hp subtracted
        * if hp goes below 0, a new pokemon has to be chosen and win condition should be checked
    """
    logger.info(f"{attacking_pokemon.name} attacks {defending_pokemon.name} with {attack_name}!")       
    sys.clear()
    print(f"{attacking_pokemon.name} used {attack_name}!")
    sys.wait_for_keypress()

    # decrement remaining attack counter
    if type == "basic":
        remaining_light = cursor.execute("SELECT remaining_light FROM team WHERE team_id = ?", (attacking_pokemon.team_id,)).fetchone()[0]
        cursor.execute("UPDATE team SET remaining_light = ? WHERE team_id = ?", (remaining_light-1, attacking_pokemon.team_id))
    else:
        remaining_special = cursor.execute("SELECT remaining_special FROM team WHERE team_id = ?", (attacking_pokemon.team_id,)).fetchone()[0]
        cursor.execute("UPDATE team SET remaining_special = ? WHERE team_id = ?", (remaining_special-1, attacking_pokemon.team_id))
    conn.commit()

    # calculate damage
    # base damage
    attack = 1
    defense = 1
    if type == "basic":
        attack = cursor.execute("SELECT attack FROM pokemon WHERE pokedex_number = ?", (attacking_pokemon.pokedex_number,)).fetchone()[0]
        defense = cursor.execute("SELECT defense FROM pokemon WHERE pokedex_number = ?", (defending_pokemon.pokedex_number,)).fetchone()[0]
    else:
        attack = cursor.execute("SELECT sp_attack FROM pokemon WHERE pokedex_number = ?", (attacking_pokemon.pokedex_number,)).fetchone()[0]
        defense = cursor.execute("SELECT sp_defense FROM pokemon WHERE pokedex_number = ?", (defending_pokemon.pokedex_number,)).fetchone()[0]
    
    level_multiplier = 110 / 5 + 2
    power = 60
    base_damage = level_multiplier * power * (attack/defense) / 50 + 2

    # type damage
    type_damage = 1
    if type != "basic":
        (defending_type1, defending_type2) = cursor.execute("SELECT type1, type2 FROM pokemon WHERE pokedex_number = ?", (defending_pokemon.pokedex_number,)).fetchone()
        type1_column = "against_" + defending_type1
        against_type1 = cursor.execute("SELECT %s FROM attacks WHERE type = ?" %(type1_column), (type,)).fetchone()[0]
        against_type2 = 1
        if defending_type2 is not None:
            type2_column = "against_" + defending_type2
            against_type2 = cursor.execute("SELECT %s FROM attacks WHERE type = ?" %(type2_column), (type,)).fetchone()[0]
        type_damage = max(against_type1, against_type2, against_type1*against_type2)
    
    # critical multiplier
    critical_mult = 1
    if random.random() < 1/10:
        print("A critical hit!")
        critical_mult = 2
    
    # random multiplier
    random_mult = random.randint(85,100) / 100

    # final damage
    damage = int(base_damage * type_damage * critical_mult * random_mult)
    print(f"{attacking_pokemon.name} did {damage} damage!")
    logger.info(f"{attacking_pokemon.name} did {damage} damage")
    sys.wait_for_keypress()   

    # inflict damage
    defending_pokemon.set_hp(defending_pokemon.get_hp() - damage)

    # check if pokemon feinted
    if defending_pokemon.get_hp() <= 0:
        print(f"{defending_pokemon.name} fainted!")
        logger.info(f"{defending_pokemon.name} fainted!")
        sys.wait_for_keypress()
        defending_player_id = cursor.execute("SELECT player_id FROM team WHERE team_id = ?", (defending_pokemon.team_id,)).fetchone()[0]

        # Check Win
        if check_win(defending_player_id):
            return

        if defending_player_id != 0:
            sys.clear()
            print("Your Pokemon fainted! You must choose a new Pokemon!")
            choose_pokemon()
        else:
            choose_bot_pokemon() 

def bot_attack():
    """
    bot_attack Bot attack function that chooses the best attack to inflict on the players pokemon

    Only works for an attack from the bot to the players pokemon!

    Args: None

    Returns: None

    Test:
        * function chooses the attack that inflicts the most damage depending on the respective Types of the pokemon
        * executes the correct attack function 
    """
    logger.info("bot is starting an attack")    
    pokedex_number = cursor.execute("SELECT pokedex_number FROM team WHERE team_id = ?", (bot_pokemon.team_id,)).fetchone()[0]
    basic_damage = cursor.execute("SELECT attack FROM pokemon WHERE pokedex_number = ?", (pokedex_number,)).fetchone()[0]

    (type1, type2) = cursor.execute("SELECT type1, type2 FROM pokemon WHERE pokedex_number = ?", (bot_pokemon.pokedex_number,)).fetchone()
    (defending_type1, defending_type2) = cursor.execute("SELECT type1, type2 FROM pokemon WHERE pokedex_number = ?", (player_pokemon.pokedex_number,)).fetchone()

    type1_column = "against_" + defending_type1
    type1_against_type1 = cursor.execute("SELECT %s FROM attacks WHERE type = ?" %(type1_column), (type1,)).fetchone()[0]
    sp_attack1 = cursor.execute("SELECT Attack FROM attacks WHERE Type = ?", (type1,)).fetchone()[0]
    
    if type2 is not None:
        type2_against_type1 = cursor.execute("SELECT %s FROM attacks WHERE type = ?" %(type1_column), (type2,)).fetchone()[0]
        sp_attack2 = cursor.execute("SELECT Attack FROM attacks WHERE Type = ?", (type2,)).fetchone()[0]

    type1_against_type2 = 1
    type2_against_type2 = 1

    if defending_type2 is not None:
        type2_column = "against_" + defending_type2
        type1_against_type2 = cursor.execute("SELECT %s FROM attacks WHERE type = ?" %(type2_column), (type1,)).fetchone()[0]
        if type2 is not None:
            type2_against_type2 = cursor.execute("SELECT %s FROM attacks WHERE type = ?" %(type2_column), (type2,)).fetchone()[0]

    type1_damage = type1_against_type1*type1_against_type2
    if type2 is not None:
        type2_damage = type2_against_type1*type2_against_type2
    else:
        type2_against_type1 = 0
        type2_against_type2 = 0
        type2_damage = 0
    

    logger.info("bot chose an attack")
    if max(type1_damage, type2_damage) < 1:
        attack_name = "Tackle"
        type = "basic"
    elif type1_damage>type2_damage:
        attack_name = sp_attack1
        type = type1
    else:
        attack_name = sp_attack2
        type = type2
    attack(attack_name, type, bot_pokemon, player_pokemon)


def check_win(player_id):
    """
    check_win Function to check if all pokemon of a player have already fainted in order to determine if the other player has won
    
    If so, prints who won the game and sets the global variable game_over to True

    Args:
        player_id (int): id whose team should be checked

    Returns:
        boolean: False if the game is not over, True if the game is over

    Test:
        * player_id should be of type int
        * global variable should be successfully accessed and changed
        * function should effectively recognize if all pokemon in the team have fainted
    """
    logger.info("checking if win conditions have been fulfilled")    
    end = True
    hp_values = cursor.execute("SELECT health FROM team WHERE player_id = ?", (player_id,)).fetchall()
    for hp in hp_values:
        if hp[0] > 0:
            end = False
    
    if end:
        is_bot = cursor.execute("SELECT is_bot FROM players WHERE player_id = ?", (player_id,)).fetchone()[0]
        if is_bot:
            logger.info("all pokemon in the enemy team fainted, you won!")
            sys.clear()
            print("You Won!")

            # calculate win rewards
            logger.info("calculating win rewards")

            alive_pokemon = teamManager.alive_team_size(current_player.id)
            old_xp = cursor.execute("SELECT xp FROM players WHERE player_id = ?", (current_player.id,)).fetchone()[0]
            lvl = cursor.execute("SELECT level FROM players WHERE player_id = ?", (current_player.id,)).fetchone()[0]
            old_dollars = cursor.execute("SELECT dollars FROM players WHERE player_id = ?", (current_player.id,)).fetchone()[0]
            old_score = cursor.execute("SELECT high_score FROM players WHERE player_id = ?", (current_player.id,)).fetchone()[0]
            

            new_xp = int(alive_pokemon*random.randint(85,100))
            new_score = new_xp * 2
            print(f"You scored {new_score} points and gained {new_xp} XP!")
            new_dollars = int(alive_pokemon*1.5*random.randint(60,100))
            if (old_xp + new_xp) > 1000: # level up!
                print("You Leveled Up!")
                old_xp = 0
                lvl = lvl + 1
                new_dollars = new_dollars + 100
            print(f"You earned {new_dollars} dollars")
            new_xp = old_xp + new_xp
            new_dollars = old_dollars + new_dollars

            # write win rewards in table
            logger.info("writing win rewards in table")
            cursor.execute("UPDATE players SET xp = ? WHERE player_id = ?", (new_xp, current_player.id))
            cursor.execute("UPDATE players SET level = ? WHERE player_id = ?", (lvl, current_player.id))
            cursor.execute("UPDATE players SET dollars = ? WHERE player_id = ?", (new_dollars, current_player.id))
            if new_score > old_score:
                cursor.execute("UPDATE players SET high_score = ? WHERE player_id = ?", (new_score, current_player.id))
            conn.commit()


            sys.wait_for_keypress()
        else:
            sys.clear()
            logger.info("all pokemon in your team fainted, you lost!")
            print("You Lost!")
            sys.wait_for_keypress()
        global game_over
        game_over = True
    return end

"""


*inputs: none
*outputs: none
"""
def fight_engine():
    """
    fight_engine Main loop to manage the fights

    - Starts by creating the bots team and choosing him a pokemon
    - Resets the players team health and remaing attacks
    - Prompts the player to choose a pokemon

    - Checks whose pokemon has a higher speed rating, lets that player go first

    - Turn based system: player and bot take turns making their move

    - Player has the option to attack (calls choose_attack) or change their current pokemon (calls choose_pokemon) or run away
    - The first to options end the turn, running away goes back to the main menu

    - The bot always calls bot_attack 

    - After each turn, the global variable game_over is checked, if True returns user to the main menu

    Args: None

    Returns: None

    Test:
        * inputs other than 1-3 should not be accepted
        * Pokemon with the higher speed stat should start
        * if all pokemon have fainted, the game should end
        * Effective turn based fight system should work
    """
    logger.info("starting main fight engine")    
    #initial set up for fight
    teamManager.create_random_team(0)
    choose_bot_pokemon()
    teamManager.heal_team(current_player.id)
    teamManager.reset_team(current_player.id)
    choose_pokemon()

    global game_over
    game_over = False 

    player_pokemon_speed = cursor.execute("SELECT speed FROM pokemon WHERE pokedex_number = ?", (player_pokemon.pokedex_number,)).fetchone()[0]
    bot_pokemon_speed = cursor.execute("SELECT speed FROM pokemon WHERE pokedex_number = ?", (bot_pokemon.pokedex_number,)).fetchone()[0]
    
    if bot_pokemon_speed > player_pokemon_speed:
        sys.clear()
        print("It's the Enemy's turn!")
        print(f"You: {player_pokemon.name: <10} hp: {player_pokemon.get_hp(): <10} Enemy: {bot_pokemon.name: <10} hp: {bot_pokemon.get_hp()}")
        sys.wait_for_keypress()
        bot_attack()

    while True:
        while True:
            sys.clear()
            print("It's your turn!")
            print(f"You: {player_pokemon.name: <10} hp: {player_pokemon.get_hp(): <10} Enemy: {bot_pokemon.name: <10} hp: {bot_pokemon.get_hp()}")
            print(" 1. Attack \n 2. Choose a different Pokemon \n 3. Run")
            decision = input("Please use the Keys 1-3 + ENTER to choose what to do next! ")
            sys.clear()

            if decision == "1":
                if choose_attack() == 0:
                    break
            elif decision == "2":
                choose_pokemon()
                break
            elif decision == "3":
                return
            else:
                print("Invalid input given!")
        
        if game_over:
            game_over = False
            return
        
        sys.clear()
        print("It's the Enemy's turn!")
        print(f"You: {player_pokemon.name: <10} hp: {player_pokemon.get_hp(): <10} Enemy: {bot_pokemon.name: <10} hp: {bot_pokemon.get_hp()}")
        sys.wait_for_keypress()
        bot_attack()

        if game_over:
            game_over = False
            return

    