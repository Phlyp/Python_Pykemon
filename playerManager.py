import sys
import os
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
import pandas as pd
import teamManager as team
import sqlite3
from database import db_name



conn = sqlite3.connect(db_name)
cursor = conn.cursor()
start_dollars = 1000
player_changed = False

"""
(abstract) class that saves the id and name of the current player for convenience
"""
class current_player:
    id = 1
    name = ""

"""
    Class for player selection menu
"""

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

    """
    prints all existing players in a gui
    allows user to choose a player from list

    *inputs: none
    *outputs: none
    """
    def createTable(self):
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

    """
    select player when double clicked

    *inputs: none
    *outputs: none
    """
    def player_double_clicked(self):
        id = self.table_widget.currentIndex().row()
        if id != 0:
            current_player.id = id
            current_player.name = cursor.execute("SELECT name FROM players WHERE player_id = ?", (current_player.id,)).fetchone()[0]
            global player_changed
            player_changed = True
            self.close()
   

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
  
    """
    creates new player if the player doesn't exist yet

    *inputs: none
    *outputs: none
    """
    def submit(self):
        name = self.player_name_textbox.text()
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
        global player_changed
        if player_changed:
            self.close()
        else:
            quit()
        

    def change_gui(self):
        global player_changed
        player_changed = False
        self.window = AppChangePlayer()


"""
    player main menu to chose between creating new player or selecting existing one
"""
class AppPlayerSettings(QMainWindow):
     # constructor
    def __init__(self):
        super().__init__()
        self.title = 'player settings'
        self.left = 900
        self.top = 300
        self.width = 320
        self.height = 140
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        # Create player info
        self.button_info = QPushButton('player info', self)
        self.button_info.move(20,100)

        # Create change player button 
        self.button_change_window = QPushButton('change player', self)
        self.button_change_window.move(120,100)

        # Create delete all players button 
        self.button_close = QPushButton('delete all players', self)
        self.button_close.move(220,100)
        
        # Create cancel button 
        self.button_close = QPushButton('delete all players', self)
        self.button_close.move(220,100)

        # connect buttons to functions
        self.button_submit.clicked.connect(self.submit)
        self.button_change_window.clicked.connect(self.change_gui)
        self.button_close.clicked.connect(self.exit)
        self.show()

"""
starts create player gui

*inputs: none
*outputs: none
"""
def player_selection():
    app = QApplication(sys.argv)
    window = AppCreateNewPlayer()
    window.show()
    app.exec_()

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
    player_selection()