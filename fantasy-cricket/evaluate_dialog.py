from PyQt5 import QtCore, QtGui, QtWidgets
import os
import sqlite3
from score_calculator import calculate_points

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(600, 500)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        
        self.label_evaluate = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(10)
        self.label_evaluate.setFont(font)
        self.label_evaluate.setAlignment(QtCore.Qt.AlignCenter)
        self.label_evaluate.setObjectName("label_evaluate")
        self.verticalLayout.addWidget(self.label_evaluate)
        
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        self.combo_team = QtWidgets.QComboBox(Dialog)
        self.combo_team.setObjectName("combo_team")
        self.horizontalLayout.addWidget(self.combo_team)
        
        self.combo_match = QtWidgets.QComboBox(Dialog)
        self.combo_match.setObjectName("combo_match")
        self.combo_match.addItem("Match1") # Dummy match options
        self.combo_match.addItem("Match2")
        self.horizontalLayout.addWidget(self.combo_match)
        
        self.verticalLayout.addLayout(self.horizontalLayout)
        
        self.line = QtWidgets.QFrame(Dialog)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_players = QtWidgets.QLabel(Dialog)
        font.setBold(True)
        self.label_players.setFont(font)
        self.label_players.setObjectName("label_players")
        self.verticalLayout_2.addWidget(self.label_players)
        
        self.list_players = QtWidgets.QListWidget(Dialog)
        self.list_players.setObjectName("list_players")
        self.verticalLayout_2.addWidget(self.list_players)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_points = QtWidgets.QLabel(Dialog)
        self.label_points.setFont(font)
        self.label_points.setObjectName("label_points")
        self.verticalLayout_3.addWidget(self.label_points)
        
        self.list_points = QtWidgets.QListWidget(Dialog)
        self.list_points.setObjectName("list_points")
        self.verticalLayout_3.addWidget(self.list_points)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        
        self.btn_calculate = QtWidgets.QPushButton(Dialog)
        self.btn_calculate.setObjectName("btn_calculate")
        self.horizontalLayout_3.addWidget(self.btn_calculate)
        
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        
        self.label_score = QtWidgets.QLabel(Dialog)
        self.label_score.setObjectName("label_score")
        self.horizontalLayout_3.addWidget(self.label_score)
        
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        
        # Connect signals
        self.btn_calculate.clicked.connect(self.calculate_score)
        
        self.load_teams()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Evaluate Team"))
        self.label_evaluate.setText(_translate("Dialog", "Evaluate the Performance of your Fantasy Team"))
        self.label_players.setText(_translate("Dialog", "Players"))
        self.label_points.setText(_translate("Dialog", "Points"))
        self.btn_calculate.setText(_translate("Dialog", "Calculate Score"))
        self.label_score.setText(_translate("Dialog", "00"))

    def load_teams(self):
        try:
            db_path = os.path.join(os.path.dirname(__file__), 'fantasy_cricket.db')
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM teams;")
            teams = cursor.fetchall()
            for team in teams:
                self.combo_team.addItem(team[0])
            conn.close()
        except sqlite3.Error as e:
            print("Database error: ", e)

    def calculate_score(self):
        team_name = self.combo_team.currentText()
        if not team_name:
            return
            
        self.list_players.clear()
        self.list_points.clear()
        
        try:
            db_path = os.path.join(os.path.dirname(__file__), 'fantasy_cricket.db')
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Get players in the team
            cursor.execute("SELECT players FROM teams WHERE name = ?;", (team_name,))
            row = cursor.fetchone()
            if not row:
                return
                
            players_str = row[0]
            players_list = players_str.split(',')
            
            total_score = 0
            
            for player in players_list:
                if not player:
                    continue
                # Fetch match stats for player
                cursor.execute("SELECT * FROM match WHERE Player = ?;", (player,))
                match_data = cursor.fetchone()
                
                player_points = 0
                if match_data:
                    player_points = calculate_points(match_data)
                    
                total_score += player_points
                
                self.list_players.addItem(player)
                self.list_points.addItem(str(player_points))
                
            self.label_score.setText(str(total_score))
            
            conn.close()
            
        except sqlite3.Error as e:
            print("Database error: ", e)

class EvaluateDialog(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(EvaluateDialog, self).__init__(parent)
        self.setupUi(self)
