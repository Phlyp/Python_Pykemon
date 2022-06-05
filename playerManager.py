"""Module Description
    * collection of functions and classes to manage the players saved in the game
    * saves currently active player with an abstract class
    * includes methods and classes to create an intuitive ui to select and create a new player

    author: Novadgaf and Phlyp
    date: 05.06.2022
    version: 1.0.0
    license: free
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtWidgets
import pandas as pd
import teamManager as team
import sqlite3
from database import db_name



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
    Class to change player
"""
class AppChangePlayer(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Player selection'
        self.left = 900
        self.top = 300
        self.width = 686
        self.height = 430
        self.initUI()
        
    def initUI(self):
        """
        initUI initializes the UI

        This UI enables the user to chose between pre created player profiles

        Args: None
        Returns: None

        Test:
            * click select player button in the AppCreateNewPlayer GUI
        """          
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.createTable()

        # Add box layout, add table to box layout and add box layout to widget
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.table_widget) 
        self.setLayout(self.layout) 

        # Show widget
        self.show()
        self.table_widget.doubleClicked.connect(self.player_double_clicked)

    def createTable(self):
        """
        createTable creates a table

        The table contains every aviable player profile and infos about the players 

        Args: None
        Returns: None

        Test:
            * check whether all non bot players from the db are in the table
        """    
       # Create table
        self.table_widget = QTableWidget()
        self.table_widget.setRowCount(cursor.execute("SELECT COUNT(player_id) FROM players WHERE is_bot = 0").fetchone()[0]+1)
        self.table_widget.setColumnCount(6)
        self.table_widget.setItem(0,0, QTableWidgetItem("player_id"))
        self.table_widget.setItem(0,1, QTableWidgetItem("name"))
        self.table_widget.setItem(0,2, QTableWidgetItem("xp"))
        self.table_widget.setItem(0,3, QTableWidgetItem("level"))
        self.table_widget.setItem(0,4, QTableWidgetItem("dollars"))
        self.table_widget.setItem(0,5, QTableWidgetItem("high_score"))

        players = cursor.execute("SELECT player_id,name,xp,level,dollars,high_score FROM players WHERE is_bot = 0").fetchall()
        
        for idxx,player in enumerate(players):
            player_id,name,xp,level,dollars,high_score = player
            idx = idxx+1
            item_player_id = QtWidgets.QTableWidgetItem(str(player_id))
            item_player_id.setFlags(item_player_id.flags() ^ QtCore.Qt.ItemIsEditable)
            self.table_widget.setItem(idx, 0, item_player_id)

            item_name = QtWidgets.QTableWidgetItem(name)
            item_name.setFlags(item_name.flags() ^ QtCore.Qt.ItemIsEditable)
            self.table_widget.setItem(idx, 1, item_name)

            item_xp = QtWidgets.QTableWidgetItem(str(xp))
            item_xp.setFlags(item_xp.flags() ^ QtCore.Qt.ItemIsEditable)
            self.table_widget.setItem(idx, 2, item_xp)

            item_level = QtWidgets.QTableWidgetItem(str(level))
            item_level.setFlags(item_level.flags() ^ QtCore.Qt.ItemIsEditable)
            self.table_widget.setItem(idx, 3, item_level)

            item_dollars = QtWidgets.QTableWidgetItem(str(dollars))
            item_dollars.setFlags(item_dollars.flags() ^ QtCore.Qt.ItemIsEditable)
            self.table_widget.setItem(idx, 4, item_dollars)

            item_high_score = QtWidgets.QTableWidgetItem(str(high_score))
            item_high_score.setFlags(item_high_score.flags() ^ QtCore.Qt.ItemIsEditable)
            self.table_widget.setItem(idx, 5, item_high_score)

            self.table_widget.setRowHeight(idx, 128)

        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def player_double_clicked(self):
        """
        player_double_clicked selects player when double clicked

        this function selects a player from the table when the user is using a double click

        Args: None
        Returns: None

        Test:
            * double click a user in the table and check whether the welcome message or the user infos are correct
        """    
        id = self.table_widget.currentIndex().row()
        if id != 0:
            current_player.id = id
            current_player.name = cursor.execute("SELECT name FROM players WHERE player_id = ?", (current_player.id,)).fetchone()[0]
            self.close()
        print(f"chose player {current_player.name}\npress close to continue")
   

"""
    player main menu to chose between creating new player or selecting existing one
"""
class AppCreateNewPlayer(QMainWindow):
     # constructor
    def __init__(self):
        super().__init__()
        self.title = 'create new player'
        self.left = 900
        self.top = 300
        self.width = 320
        self.height = 140
        self.initUI()
    
    def initUI(self):
        """
        initUI initializes the UI

        This UI enables the user to create a new user or open a GUI to choose between existing profiles

        Args: None
        Returns: None

        Test:
            * start the game or click change player button in player setting GUI
        """    
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
    
        # Create textbox + info text for name
        self.player_name_label = QLabel("player name", self)
        self.player_name_label.move(20, 20)
        self.player_name_textbox = QLineEdit(self)
        self.player_name_textbox.move(20, 50)
        self.player_name_textbox.resize(185,20)
        
        # Create submit button 
        self.button_submit = QPushButton('create player', self)
        self.button_submit.move(20,100)

        # Create select player button 
        self.button_change_window = QPushButton('select player', self)
        self.button_change_window.move(120,100)

        # Create cancel button 
        self.button_close = QPushButton('close', self)
        self.button_close.move(220,100)
        
        # connect buttons to functions
        self.button_submit.clicked.connect(self.submit)
        self.button_change_window.clicked.connect(self.change_gui)
        self.button_close.clicked.connect(self.exit)
        self.show()
  
    def closeEvent(self, event):
        """
        closeEvent called when the function self.close() is called or the user is trying to close the GUI using the x in the top right corner

        if the user didn't chose or create a player exit the program otherwise close the GUI

        Args: None
        Returns: None

        Test:
            * close the GUI without chosing / creating a player -> program ends otherwise GUI will close and program will continue
        """    
        if current_player.name == "":
            quit()

    def submit(self):
        """
        submit creates new player

        tries to create a new player if the player doesn't exist yet and the input is valid -> != ""

        Args: None
        Returns: None

        Test:
            * type nothing / something in the textfield and click create player -> fail message / new player will be created if he doesn't exist yet and continue to main menu
        """    
        name = self.player_name_textbox.text()
        if name == "":
            print('Please enter a valid name!')  
            return
        cursor.execute("SELECT COUNT(*) FROM players WHERE name = ?", (name,))
        if cursor.fetchone()[0] > 0:
            print('Name already exists! Please enter a new name!')
        else:
            cursor.execute("INSERT INTO players(name, is_bot, xp, level, dollars, high_score) VALUES(?,0,0,0,?,0)", (name, start_dollars))
            conn.commit()
            player_id = cursor.execute("SELECT player_id FROM players WHERE name = ?", (name,)).fetchone()[0]
            current_player.id = player_id
            current_player.name = cursor.execute("SELECT name FROM players WHERE player_id = ?", (player_id,)).fetchone()[0]
            self.close()
    

    """
    go back to create new player / change player window

    *inputs: none
    *outputs: none
    """
    def exit(self):
        """
        exit called when user clicks close

        calls the function close() --> closeEvent()

        Args: None
        Returns: None

        Test:
            * click close button program will end if no new user with valid name created and no existing user selected or continue with the created / selected user
        """    
        self.close()
        

    def change_gui(self):
        """
        change_gui called when user clicks select player button

        opens AppChangePlayer GUI

        Args: None
        Returns: None

        Test:
            * click select player button player selection GUI will appear
        """    
        self.window = AppChangePlayer()


"""
    player menu to chose between several actions
"""
class AppPlayerSettings(QMainWindow):
     # constructor
    def __init__(self):
        super().__init__()
        self.title = 'player settings'
        self.left = 900
        self.top = 300
        self.width = 545
        self.height = 300
        self.initUI()
    
    def initUI(self):
        """
        initUI initializes the UI

        This UI enables the user interact with user profile settings / infos

        Args: None
        Returns: None

        Test:
            * go into Player Settings by pressing 1 + enter in the main menu 
        """    
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        # Create player info
        self.button_info = QPushButton('player info', self)
        self.button_info.move(20,20)

        # Create change player button 
        self.button_change_player = QPushButton('change player', self)
        self.button_change_player.move(120,20)

        # Create delete all players button 
        self.button_delete_all_players = QPushButton('delete all players', self)
        self.button_delete_all_players.move(220,20)
        
        # Create back button 
        self.button_back = QPushButton('back', self)
        self.button_back.move(320,20)

        # Create exit button 
        self.button_exit = QPushButton('exit game', self)
        self.button_exit.move(420,20)

        # connect buttons to functions
        self.button_info.clicked.connect(self.info)
        self.button_change_player.clicked.connect(self.change_player)
        self.button_delete_all_players.clicked.connect(self.delete_all_players)
        self.button_back.clicked.connect(self.back)
        self.button_exit.clicked.connect(self.exit)

        # create text area for user info
        self.info_area = QPlainTextEdit(self)
        self.info_area.move(20, 100)
        self.info_area.resize(505, 150)
        self.info_area.insertPlainText("press info to reveal your stats")
        self.info_area.setReadOnly(True)
        self.show()


    def info(self):
        """
        info called when user clicks player info

        player info will appear in the text area

        Args: None
        Returns: None

        Test:
            * click the player info button and check the text area for user name, xp, level, dollars, high score
        """    
        info = cursor.execute("SELECT player_id,name,xp,level,dollars,high_score FROM players WHERE player_id = ?", (current_player.id,)).fetchone()
        self.info_area.setPlainText(f"\nName: {info[1]} \nXp: {info[2]} \nLevel: {info[3]} \nDollars: {info[4]} \nHigh Score: {info[5]}")

    def change_player(self):
        """
        change_player called when user clicks change player

        AppCreateNewPlayer GUI will appear

        Args: None
        Returns: None

        Test:
            * click the change player button
        """ 
        self.window = AppCreateNewPlayer()

    def delete_all_players(self):
        """
        delete_all_players called when user clicks delete all players

        deletes all players from the database and lets the user create a new one

        Args: None
        Returns: None

        Test:
            * click the delete all players button
        """ 
        cursor.execute("DELETE FROM players WHERE is_bot = 0")
        conn.commit()
        team.delete_all_teams()
        current_player.name = ""
        self.window = AppCreateNewPlayer()

    def back(self):
        """
        back called when user clicks back

        gets the user back to the main menu

        Args: None
        Returns: None

        Test:
            * click the back button
        """ 
        self.close()

    def exit(self):
        """
        back called when user clicks exit

        ends the program

        Args: None
        Returns: None

        Test:
            * click the exit button
        """ 
        quit()
    


def player_selection():
    """
    player_selection function to initialize the AppCreateNewPlayer GUI

    Args: None
    Returns: None

    Test:
        * start the program
    """ 
    app = QApplication(sys.argv)
    window = AppCreateNewPlayer()
    window.show()
    app.exec_()


def player_exists(player_id):
    """
    player_exists Checks if a player with a given id exists in the players table

    Args:
        player_id (int): id of the player whose existence should be checked

    Returns:
        boolean: True if player has 1 entry in players table, False otherwise

    Test:
        * player_id should be of type int
        * should correctly recognize if the player exists or not
    """
    if type(player_id) != int:
        print("Error: player_id should be of type int")
        print("Exiting game")
        exit()

    cursor.execute("SELECT * FROM players WHERE player_id = ?", (player_id,))
    entries = len(cursor.fetchall())
    if entries == 1:
        return True
    return False

  
def player_settings():
    """
    player_selection function to initialize the AppPlayerSettings GUI

    Args: None
    Returns: None

    Test:
        * select Player Settings in the main menu by using the input 1+enter 
    """ 
    app = QApplication(sys.argv)
    window = AppPlayerSettings()
    window.show()
    app.exec()

