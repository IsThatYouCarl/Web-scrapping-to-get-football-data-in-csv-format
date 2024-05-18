import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QComboBox, QLabel, QLineEdit, QFileDialog, QWidget
import datscrap
from url_data import League_groups, Age_group, Position_groups, Main_position_list, Seasons, Nationality_list, Leagues
import os


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Football data scraping")
        self.setGeometry(100, 100, 700, 300)

        self.button1 = QPushButton('Get League Table', self)
        self.button1.setGeometry(150, 50, 200, 50)
        self.button1.clicked.connect(self.go_to_page1)

        self.button2 = QPushButton('Get Top Scorer', self)
        self.button2.setGeometry(150, 150, 200, 50)
        self.button2.clicked.connect(self.go_to_page2)

    def go_to_page1(self):
        # Redirect to page 1
        self.page1 = Page1()
        self.page1.show()
        self.hide()

    def go_to_page2(self):
        # Redirect to page 2
        self.page2 = Page2()
        self.page2.show()
        self.hide()


class Page1(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("League Table")
        self.setGeometry(200, 200, 700, 300)

        self.label = QLabel("Select the league:", self)
        self.label.setGeometry(50, 20, 200, 30)

        self.dropdown_league = QComboBox(self)
        self.dropdown_league.setGeometry(50, 50, 200, 30)
        for key, value in Leagues.items():
            self.dropdown_league.addItem(f'{key}')


        self.label2 = QLabel("From:", self)
        self.label2.setGeometry(50, 75, 200, 30)
        self.dropdown2 = QComboBox(self)
        self.dropdown2.setGeometry(50, 100, 200, 30)
        for key, value in Seasons.items():
            self.dropdown2.addItem(key)

        self.label3 = QLabel("To:", self)
        self.label3.setGeometry(250, 75, 200, 30)
        self.dropdown3 = QComboBox(self)
        self.dropdown3.setGeometry(250, 100, 200, 30)
        for key, value in Seasons.items():
            self.dropdown3.addItem(key)


        self.scrap_button = QPushButton("Scrap", self)
        self.scrap_button.setGeometry(50, 150, 200, 30)
        self.scrap_button.clicked.connect(self.execute_scrap_function)

        self.back_button = QPushButton("🔙", self)
        self.back_button.setGeometry(0, 0, 20, 20)
        self.back_button.clicked.connect(self.go_back)


    def execute_scrap_function(self):
        League_option_item = self.dropdown_league.currentText()
        start_year_item = Seasons[self.dropdown2.currentText()]
        end_year_item = Seasons[self.dropdown3.currentText()]

        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(self, "Save file", f'{League_option_item}-league-tables.csv', "CSV Files (*.csv);;All Files(*)")
        print(file_path)

        datscrap.get_league_table(League_option_item, start_year_item, end_year_item, file_path)

    def go_back(self):
        main_window.show()
        self.hide()

class Page2(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Top Scorer")
        self.setGeometry(200, 200, 700, 300)

        self.label = QLabel("Season:", self)
        self.label.setGeometry(50, 20, 75, 30)
        self.dropdown1 = QComboBox(self)
        self.dropdown1.setGeometry(50, 50, 75, 30)
        for key, value in Seasons.items():
            self.dropdown1.addItem(f'{key}')

        self.label2 = QLabel("League group:", self)
        self.label2.setGeometry(125, 20, 100, 30)
        self.dropdown2 = QComboBox(self)
        self.dropdown2.setGeometry(125, 50, 325, 30)
        for key, value in League_groups.items():
            self.dropdown2.addItem(key)

        self.label3 = QLabel("Nationality:", self)
        self.label3.setGeometry(450, 20, 100, 30)
        self.dropdown3 = QComboBox(self)
        self.dropdown3.setGeometry(450, 50, 200, 30)
        for key, value in Nationality_list.items():
            self.dropdown3.addItem(key)

        self.label4 = QLabel("Age Group:", self)
        self.label4.setGeometry(50, 90, 75, 30)
        self.dropdown4 = QComboBox(self)
        self.dropdown4.setGeometry(50, 120, 200, 30)
        for key, value in Age_group.items():
            self.dropdown4.addItem(key)

        self.label5 = QLabel("Position:", self)
        self.label5.setGeometry(250, 90, 75, 30)
        self.dropdown5 = QComboBox(self)
        self.dropdown5.setGeometry(250, 120, 200, 30)
        for key, value in Position_groups.items():
            self.dropdown5.addItem(key)

        self.label6 = QLabel("Main Position:", self)
        self.label6.setGeometry(450, 90, 75, 30)
        self.dropdown6 = QComboBox(self)
        self.dropdown6.setGeometry(450, 120, 200, 30)
        for key, value in Main_position_list.items():
            self.dropdown6.addItem(key)


        self.label7 = QLabel("Number of pages(Each page contains 20 players):", self)
        self.label7.setGeometry(50, 150, 300, 30)

        self.number_input = QLineEdit(self)
        self.number_input.setGeometry(50, 180, 200, 30)
        self.number_input.setText("All")
        

        self.scrap_button = QPushButton("Scrap", self)
        self.scrap_button.setGeometry(50, 220, 200, 30)
        self.scrap_button.clicked.connect(self.execute_scrap_function)

        self.back_button = QPushButton("🔙", self)
        self.back_button.setGeometry(0, 0, 20, 20)
        self.back_button.clicked.connect(self.go_back)

    def execute_scrap_function(self):
        if self.number_input.text().lower() == "all" or self.number_input.text() == "":
            page = "All"
            file_dialog = QFileDialog()
            file_path, _ = file_dialog.getSaveFileName(self, "Save file", 'top_scorer.csv', "CSV Files (*.csv);;All Files(*)")
            print(file_path)
            datscrap.get_topscorer(self.dropdown1.currentText(), self.dropdown2.currentText(), 
                               self.dropdown3.currentText(), self.dropdown4.currentText(), 
                               self.dropdown5.currentText(), self.dropdown6.currentText(), page, file_path)

        elif self.number_input.text().isdigit():
            page = int(self.number_input.text())
            file_dialog = QFileDialog()
            file_path, _ = file_dialog.getSaveFileName(self, "Save file", 'top_scorer.csv', "CSV Files (*.csv);;All Files(*)")
            datscrap.get_topscorer(self.dropdown1.currentText(), self.dropdown2.currentText(), 
                               self.dropdown3.currentText(), self.dropdown4.currentText(), 
                               self.dropdown5.currentText(), self.dropdown6.currentText(), page, file_path)
        else:
            print("Invalid input")
    
    def go_back(self):
        main_window.show()
        self.hide()

app = QApplication(sys.argv)
widget = QWidget()
main_window = MainWindow()
main_window.show()

sys.exit(app.exec())