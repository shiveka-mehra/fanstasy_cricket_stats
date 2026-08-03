import sys
import os
import sqlite3
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QInputDialog
from evaluate_dialog import EvaluateDialog

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        
        # Selections count
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setTitle("Your Selections")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)
        
        self.lbl_bat = QtWidgets.QLabel("Batsmen (BAT) 0")
        self.horizontalLayout.addWidget(self.lbl_bat)
        self.lbl_bow = QtWidgets.QLabel("Bowlers (BOW) 0")
        self.horizontalLayout.addWidget(self.lbl_bow)
        self.lbl_ar = QtWidgets.QLabel("Allrounders (AR) 0")
        self.horizontalLayout.addWidget(self.lbl_ar)
        self.lbl_wk = QtWidgets.QLabel("Wicket-keeper (WK) 0")
        self.horizontalLayout.addWidget(self.lbl_wk)
        
        self.verticalLayout.addWidget(self.groupBox)
        
        # Points info
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.lbl_points_avail = QtWidgets.QLabel("Points Available 1200")
        self.horizontalLayout_2.addWidget(self.lbl_points_avail)
        self.lbl_points_used = QtWidgets.QLabel("Points Used 0")
        self.horizontalLayout_2.addWidget(self.lbl_points_used)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        
        # List widgets and Radio buttons
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        
        # Left side
        self.verticalLayout_left = QtWidgets.QVBoxLayout()
        self.horizontalLayout_rad = QtWidgets.QHBoxLayout()
        self.rad_bat = QtWidgets.QRadioButton("BAT")
        self.rad_bat.setChecked(True)
        self.horizontalLayout_rad.addWidget(self.rad_bat)
        self.rad_bow = QtWidgets.QRadioButton("BOW")
        self.horizontalLayout_rad.addWidget(self.rad_bow)
        self.rad_ar = QtWidgets.QRadioButton("AR")
        self.horizontalLayout_rad.addWidget(self.rad_ar)
        self.rad_wk = QtWidgets.QRadioButton("WK")
        self.horizontalLayout_rad.addWidget(self.rad_wk)
        
        self.verticalLayout_left.addLayout(self.horizontalLayout_rad)
        self.list_available = QtWidgets.QListWidget()
        self.verticalLayout_left.addWidget(self.list_available)
        
        self.horizontalLayout_3.addLayout(self.verticalLayout_left)
        
        # Arrow buttons
        self.verticalLayout_arrows = QtWidgets.QVBoxLayout()
        self.btn_add = QtWidgets.QPushButton(">")
        self.btn_remove = QtWidgets.QPushButton("<")
        
        # Style the buttons to make them look like arrows
        arrow_style = "font-weight: bold; font-size: 16px; padding: 5px; width: 30px;"
        self.btn_add.setStyleSheet(arrow_style)
        self.btn_remove.setStyleSheet(arrow_style)
        
        self.verticalLayout_arrows.addStretch()
        self.verticalLayout_arrows.addWidget(self.btn_add)
        self.verticalLayout_arrows.addWidget(self.btn_remove)
        self.verticalLayout_arrows.addStretch()
        
        self.horizontalLayout_3.addLayout(self.verticalLayout_arrows)
        # Right side
        self.verticalLayout_right = QtWidgets.QVBoxLayout()
        self.lbl_team_name = QtWidgets.QLabel("Team Name ")
        self.verticalLayout_right.addWidget(self.lbl_team_name)
        self.list_selected = QtWidgets.QListWidget()
        self.verticalLayout_right.addWidget(self.list_selected)
        
        self.horizontalLayout_3.addLayout(self.verticalLayout_right)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        
        MainWindow.setCentralWidget(self.centralwidget)
        
        # Menu Bar
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menuManage_Teams = QtWidgets.QMenu(self.menubar)
        self.menuManage_Teams.setTitle("Manage Teams")
        
        self.actionNEW_Team = QtWidgets.QAction(MainWindow)
        self.actionNEW_Team.setText("NEW Team")
        self.menuManage_Teams.addAction(self.actionNEW_Team)
        
        self.actionOPEN_Team = QtWidgets.QAction(MainWindow)
        self.actionOPEN_Team.setText("OPEN Team")
        self.menuManage_Teams.addAction(self.actionOPEN_Team)
        
        self.actionSAVE_Team = QtWidgets.QAction(MainWindow)
        self.actionSAVE_Team.setText("SAVE Team")
        self.menuManage_Teams.addAction(self.actionSAVE_Team)
        
        self.actionEVALUATE_Team = QtWidgets.QAction(MainWindow)
        self.actionEVALUATE_Team.setText("EVALUATE Team")
        self.menuManage_Teams.addAction(self.actionEVALUATE_Team)
        
        self.menubar.addAction(self.menuManage_Teams.menuAction())
        MainWindow.setMenuBar(self.menubar)

        MainWindow.setWindowTitle("Fantasy Cricket")

class MainApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainApp, self).__init__()
        self.setupUi(self)
        
        # Apply Styling
        self.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
                color: #333;
            }
            QGroupBox {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 5px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 5px;
                color: #495057;
                font-weight: bold;
            }
            QListWidget {
                border: 1px solid #ced4da;
                border-radius: 5px;
                padding: 5px;
                background-color: #ffffff;
            }
            QListWidget::item {
                padding: 5px;
            }
            QListWidget::item:selected {
                background-color: #0d6efd;
                color: white;
            }
            QPushButton {
                background-color: #0d6efd;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #0b5ed7;
            }
        """)
        
        # Game State Variables
        self.bat = 0
        self.bow = 0
        self.ar = 0
        self.wk = 0
        self.points_avail = 1200
        self.points_used = 0
        self.team_name = ""
        
        # Store players data from DB
        self.players_data = {}
        
        self.connect_signals()
        
    def connect_signals(self):
        self.actionNEW_Team.triggered.connect(self.new_team)
        self.actionOPEN_Team.triggered.connect(self.open_team)
        self.actionSAVE_Team.triggered.connect(self.save_team)
        self.actionEVALUATE_Team.triggered.connect(self.evaluate_team)
        
        self.rad_bat.toggled.connect(self.populate_available)
        self.rad_bow.toggled.connect(self.populate_available)
        self.rad_ar.toggled.connect(self.populate_available)
        self.rad_wk.toggled.connect(self.populate_available)
        
        self.list_available.itemDoubleClicked.connect(self.add_player)
        self.list_selected.itemDoubleClicked.connect(self.remove_player)
        
        self.btn_add.clicked.connect(self.add_player_btn)
        self.btn_remove.clicked.connect(self.remove_player_btn)

    def load_players_from_db(self):
        try:
            db_path = os.path.join(os.path.dirname(__file__), 'fantasy_cricket.db')
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT player, value, ctg FROM stats")
            rows = cursor.fetchall()
            self.players_data = {row[0]: {'value': row[1], 'ctg': row[2]} for row in rows}
            conn.close()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Database error: {e}")

    def update_counts(self):
        self.lbl_bat.setText(f"Batsmen (BAT) {self.bat}")
        self.lbl_bow.setText(f"Bowlers (BOW) {self.bow}")
        self.lbl_ar.setText(f"Allrounders (AR) {self.ar}")
        self.lbl_wk.setText(f"Wicket-keeper (WK) {self.wk}")
        self.lbl_points_avail.setText(f"Points Available {self.points_avail}")
        self.lbl_points_used.setText(f"Points Used {self.points_used}")

    def new_team(self):
        text, ok = QInputDialog.getText(self, 'Team Name', 'Enter name of team:')
        if ok and text:
            self.team_name = text
            self.lbl_team_name.setText(f"Team Name {self.team_name}")
            self.bat = 0
            self.bow = 0
            self.ar = 0
            self.wk = 0
            self.points_avail = 1200
            self.points_used = 0
            self.list_selected.clear()
            self.load_players_from_db()
            self.update_counts()
            self.populate_available()

    def open_team(self):
        try:
            db_path = os.path.join(os.path.dirname(__file__), 'fantasy_cricket.db')
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM teams;")
            teams = [row[0] for row in cursor.fetchall()]
            conn.close()
            
            if not teams:
                QMessageBox.information(self, "Info", "No saved teams found.")
                return
                
            team, ok = QInputDialog.getItem(self, "Open Team", "Choose a team", teams, 0, False)
            if ok and team:
                self.team_name = team
                self.lbl_team_name.setText(f"Team Name {self.team_name}")
                self.load_team_data(team)
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Database error: {e}")

    def load_team_data(self, team_name):
        try:
            db_path = os.path.join(os.path.dirname(__file__), 'fantasy_cricket.db')
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT players, value FROM teams WHERE name = ?;", (team_name,))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                players_str, value_used = row
                players = players_str.split(',')
                
                self.bat = 0
                self.bow = 0
                self.ar = 0
                self.wk = 0
                self.points_used = 0
                
                self.load_players_from_db()
                self.list_selected.clear()
                
                for p in players:
                    if p in self.players_data:
                        self.list_selected.addItem(f"{p} [{self.players_data[p]['value']}]")
                        self.points_used += self.players_data[p]['value']
                        ctg = self.players_data[p]['ctg']
                        if ctg == 'BAT': self.bat += 1
                        elif ctg == 'BOW': self.bow += 1
                        elif ctg == 'AR': self.ar += 1
                        elif ctg == 'WK': self.wk += 1
                        
                self.points_avail = 1200 - self.points_used
                self.update_counts()
                self.populate_available()
                
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Database error: {e}")

    def save_team(self):
        if not self.team_name:
            QMessageBox.warning(self, "Warning", "No team created. Use 'NEW Team' to create one.")
            return
            
        count = self.list_selected.count()
        if count != 11:
            QMessageBox.warning(self, "Warning", f"A team must have exactly 11 players. You have {count}.")
            return
            
        players = []
        for i in range(count):
            players.append(self.list_selected.item(i).text().split(' [')[0])
            
        players_str = ",".join(players)
        
        try:
            db_path = os.path.join(os.path.dirname(__file__), 'fantasy_cricket.db')
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Check if team exists
            cursor.execute("SELECT name FROM teams WHERE name = ?", (self.team_name,))
            if cursor.fetchone():
                cursor.execute("UPDATE teams SET players = ?, value = ? WHERE name = ?", (players_str, self.points_used, self.team_name))
            else:
                cursor.execute("INSERT INTO teams (name, players, value) VALUES (?, ?, ?)", (self.team_name, players_str, self.points_used))
                
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Success", "Team saved successfully!")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Database error: {e}")

    def evaluate_team(self):
        dialog = EvaluateDialog(self)
        dialog.exec_()

    def get_selected_category(self):
        if self.rad_bat.isChecked(): return "BAT"
        if self.rad_bow.isChecked(): return "BOW"
        if self.rad_ar.isChecked(): return "AR"
        if self.rad_wk.isChecked(): return "WK"

    def populate_available(self):
        if not self.team_name:
            return
            
        ctg = self.get_selected_category()
        self.list_available.clear()
        
        selected_players = []
        for i in range(self.list_selected.count()):
            selected_players.append(self.list_selected.item(i).text().split(' [')[0])
            
        for player, data in self.players_data.items():
            if data['ctg'] == ctg and player not in selected_players:
                self.list_available.addItem(f"{player} [{data['value']}]")

    def add_player(self, item):
        player = item.text()
        self.process_add_player(player, item)

    def add_player_btn(self):
        item = self.list_available.currentItem()
        if item:
            self.add_player(item)
        else:
            QMessageBox.warning(self, "Warning", "Please select a player to add.")

    def process_add_player(self, player_text, item):
        player = player_text.split(' [')[0]
        data = self.players_data[player]
        ctg = data['ctg']
        val = data['value']
        
        # Validation rules
        if self.list_selected.count() >= 11:
            QMessageBox.critical(self, "Error", "You can't select more than 11 players.")
            return
            
        if self.points_avail < val:
            QMessageBox.critical(self, "Error", "Not enough points available!")
            return
            
        if ctg == 'WK' and self.wk >= 1:
            QMessageBox.critical(self, "Error", "You can't select more than one wicket-keeper.")
            return
        if ctg == 'BAT' and self.bat >= 5:
            QMessageBox.critical(self, "Error", "You can't select more than 5 batsmen.")
            return
        if ctg == 'BOW' and self.bow >= 5:
            QMessageBox.critical(self, "Error", "You can't select more than 5 bowlers.")
            return
        if ctg == 'AR' and self.ar >= 3:
            QMessageBox.critical(self, "Error", "You can't select more than 3 allrounders.")
            return
            
        # Add player
        self.list_available.takeItem(self.list_available.row(item))
        self.list_selected.addItem(player_text)
        
        self.points_avail -= val
        self.points_used += val
        
        if ctg == 'BAT': self.bat += 1
        elif ctg == 'BOW': self.bow += 1
        elif ctg == 'AR': self.ar += 1
        elif ctg == 'WK': self.wk += 1
        
        self.update_counts()

    def remove_player(self, item):
        player = item.text()
        self.process_remove_player(player, item)

    def remove_player_btn(self):
        item = self.list_selected.currentItem()
        if item:
            self.remove_player(item)
        else:
            QMessageBox.warning(self, "Warning", "Please select a player to remove.")

    def process_remove_player(self, player_text, item):
        player = player_text.split(' [')[0]
        data = self.players_data[player]
        ctg = data['ctg']
        val = data['value']
        
        self.list_selected.takeItem(self.list_selected.row(item))
        
        if ctg == self.get_selected_category():
            self.list_available.addItem(player_text)
            
        self.points_avail += val
        self.points_used -= val
        
        if ctg == 'BAT': self.bat -= 1
        elif ctg == 'BOW': self.bow -= 1
        elif ctg == 'AR': self.ar -= 1
        elif ctg == 'WK': self.wk -= 1
        
        self.update_counts()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())
