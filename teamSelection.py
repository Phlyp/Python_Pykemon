"""Module Description
    * module that allows the player to manually choose which pokemon to add to his team
    * Uses PyQT5 to open a widget with a table structure that the user can scroll through to view and select pokemon

    author: Phlyp, Novadgaf and hipman8
    date: 05.06.2022
    version: 1.0.0
    license: free
"""

import sys
import os
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
import pandas as pd
import teamManager as team
from playerManager import player_exists

class App(QWidget):
    """
    Class for pokemon selection menu
    """

    # constructor
    def __init__(self, player_id):
        super().__init__()
        self.title = 'Pokemon List'
        self.left = 900
        self.top = 300
        self.width = 686
        self.height = 430
        self.df_pokemon = pd.read_csv('Data/pokemon.csv')
        self.count = 1
        self.player_id = player_id
        self.initUI()
        
    def initUI(self):
        """
        initUI Initialises the graphical Widget to choose the pokemon

        Args: None

        Returns: None

        Test:
            * successfully creates a widget window
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
        self.table_widget.doubleClicked.connect(self.pokemon_double_clicked)

    def createTable(self):
        """
        createTable Creates a basic graphical table to choose the pokemon

        Args: None

        Returns: None

        Test:
            * successfully shows a table with all pokemon
        """        
       # Create table
        self.table_widget = QTableWidget()
        self.table_widget.setRowCount(721)
        self.table_widget.setColumnCount(2)
        #Get image filenames
        image_files = [f for f in os.listdir('Data/pokemon_images/pokemon/pokemon') if os.path.isfile(os.path.join('Data/pokemon_images/pokemon/pokemon', f))]
        for idx, name in enumerate(self.df_pokemon.name):
            image_name = str(idx+1) + '.png'
            #Some Pokemon have different Forms so the images are labeled differently which needs to be checked
            if image_name not in image_files:
                image_name = next(x for x in image_files if (str(idx+1) + '-' in x))
            image_path = f'Data/pokemon_images/pokemon/pokemon/{image_name}'
            pic = QtGui.QPixmap(image_path)
            picture_label = QtWidgets.QLabel()
            picture_label.setPixmap(pic)
            item = QtWidgets.QTableWidgetItem(name)
            item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
            #Fill column 1 with names of pokemon and column 2 with their corresponding picture
            self.table_widget.setItem(idx, 0, item)
            self.table_widget.setCellWidget(idx, 1, picture_label)
            self.table_widget.setRowHeight(idx, 256)
            if idx == 720:
                break
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def pokemon_double_clicked(self):
        """
        pokemon_double_clicked Function checks if a field in the table has been double clicked and adds that pokemon to the team

        Args: None

        Returns: None

        Test:
            * a double click should add the pokemon to the players team
        """        
        self.poke_ID = self.table_widget.currentIndex().row()
        team.add_pokemon_to_team(self.player_id, self.poke_ID, self.count)
        self.count += 1
        if self.count == 7:
            self.close()

    
def start_selection(player_id):
    """
    start_selection _summary_

    Args:
        player_id (int): _description_
    
    Returns: None

    Test:
        * player_id should be of type int
        * player should exist
        * successfully starts the selection process
    """    
    if type(player_id) != int:
        print("Error: player_id should be of type int")
        print("Exiting game")
        exit()
    if player_exists(player_id) == False:
        print("Error: player does not exist")
        print("Exiting game")
        exit()
        
    app = QApplication(sys.argv)
    ex = App(player_id)
    app.exec_()