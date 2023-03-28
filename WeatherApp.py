from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from pymongo import *
import sys, requests, certifi

from Ui_weather_main import *


class Main_Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Main_Window, self).__init__()
        self.setupUi(self)
        # connection = "mongodb+srv://melike:1234@weatherapp.6zi3pge.mongodb.net/Configurations?retryWrites=true&w=majority"
        connection = "mongodb+srv://melike:1234@weatherapp.xzog7un.mongodb.net/?retryWrites=true&w=majority"
        client = MongoClient(connection, tlsCAFile=certifi.where())
        db = client.get_database ('WeatherApp')
        self.weather_records = db.weather
        self.countries_records = db.countries_data

        self.BEupdate_city()
        self.city_name = self.main_tbl_cities.item(0, 0).text()
        self.country_name = "BE"
        self.take_info()
        self.update_weather()

        self.main_btn_search.clicked.connect(self.search_city)
        self.main_btn_exit.clicked.connect(self.exit)

        self.main_btn_belgium.clicked.connect(self.BEupdate_city)
        self.main_btn_germany.clicked.connect(self.DEupdate_city)
        self.main_btn_usa.clicked.connect(self.USupdate_city)
        self.main_tbl_cities.itemClicked.connect(self.clicked_city)

        self.main_btn_info.clicked.connect(self.info)
    
    def clicked_city(self):
            indexes = []
            for selectionRange in self.main_tbl_cities.selectedRanges():
                indexes.extend(range(selectionRange.topRow(), selectionRange.bottomRow()+1))
                for i in indexes:
                    self.city_name = self.main_tbl_cities.item(i, 0).text()
                    self.take_info()
                    self.update_weather()
                    self.main_lbl_searchwarning.hide()
                    self.main_linedit_city.clear()
    
    def search_city(self):
        self.city_name = (self.main_linedit_city.text()).title()
        query = {"city_name": self.city_name}
        reader = self.countries_records.find (query, {'city_name': 1})
        data_list = [data['city_name'] for data in reader]

        if self.city_name in data_list:
            self.take_info()
            self.update_weather()
            self.main_lbl_searchwarning.hide()
        else:
            self.main_lbl_searchwarning.show()
            self.main_lbl_searchwarning.setText("Incorrect city name!")

    def take_info(self):
        reader = self.countries_records.find({"city_name":self.city_name},{'country_name': 1, "state_name":1, 'population': 1})
        data_list = []
        for data in reader:
            data_list.append(data)
        for data in data_list:
            self.main_lbl_showcityname.setText(self.city_name)
            self.main_lbl_showstate.setText(data["state_name"])
            self.main_lbl_showpopulation.setText(str(data["population"]))
            self.country_name = data["country_name"]
            if self.country_name == "BE":
                self.main_lbl_showcountry.setText("Belgium")
            elif self.country_name == "DE":
                self.main_lbl_showcountry.setText("Germany")
            elif self.country_name == "US":
                self.main_lbl_showcountry.setText("United States of America")
 
    def BEupdate_city(self):
        # mongodb den şehir çek
        reader = self.countries_records.find({"country_name":"BE"},{'city_name': 1, "state_name":1, 'population': 1})
        data_list = []
        for data in reader:
            data_list.append(data)
        
        row = 0
        self.main_tbl_cities.setRowCount(len(data_list))
        for data in data_list:
            self.main_tbl_cities.setItem(row, 0, QtWidgets.QTableWidgetItem(data["city_name"]))
            self.main_tbl_cities.setItem(row, 1, QtWidgets.QTableWidgetItem(data["state_name"]))
            self.main_tbl_cities.setItem(row, 2, QtWidgets.QTableWidgetItem(str(data["population"]))) 
            row += 1
        self.main_btn_belgium.setStyleSheet("background-color: rgba(255,255,255,0.95);")
        self.main_btn_germany.setStyleSheet("background-color: rgba(255,255,255,0.7);")
        self.main_btn_usa.setStyleSheet("background-color: rgba(255,255,255,0.7);")

    def DEupdate_city(self):
        reader = self.countries_records.find({"country_name":"DE"},{'city_name': 1, "state_name":1, 'population': 1})
        data_list = []
        for data in reader:
            data_list.append(data)
     
        row = 0
        self.main_tbl_cities.setRowCount(len(data_list))
        for data in data_list:
            self.main_tbl_cities.setItem(row, 0, QtWidgets.QTableWidgetItem(data["city_name"]))
            self.main_tbl_cities.setItem(row, 1, QtWidgets.QTableWidgetItem(data["state_name"]))
            self.main_tbl_cities.setItem(row, 2, QtWidgets.QTableWidgetItem(str(data["population"]))) 
            row += 1
        self.main_btn_germany.setStyleSheet("background-color: rgba(255,255,255,0.95);")
        self.main_btn_belgium.setStyleSheet("background-color: rgba(255,255,255,0.7);")
        self.main_btn_usa.setStyleSheet("background-color: rgba(255,255,255,0.7);")

    def USupdate_city(self):
        reader = self.countries_records.find({"country_name":"US"},{'city_name': 1, "state_name":1, 'population': 1})
        data_list = []
        for data in reader:
            data_list.append(data)
     
        row = 0
        self.main_tbl_cities.setRowCount(len(data_list))
        for data in data_list:
            self.main_tbl_cities.setItem(row, 0, QtWidgets.QTableWidgetItem(data["city_name"]))
            self.main_tbl_cities.setItem(row, 1, QtWidgets.QTableWidgetItem(data["state_name"]))
            self.main_tbl_cities.setItem(row, 2, QtWidgets.QTableWidgetItem(str(data["population"]))) 
            row += 1
        self.main_btn_usa.setStyleSheet("background-color: rgba(255,255,255,0.95);")
        self.main_btn_germany.setStyleSheet("background-color: rgba(255,255,255,0.7);")
        self.main_btn_belgium.setStyleSheet("background-color: rgba(255,255,255,0.7);")

    def update_weather(self):
        city_name = self.city_name
        country_code = self.country_name

        API_key = '38a18d9e8231ce64548938b0187511ce'
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name},{country_code}&appid={API_key}&units=metric'

        try:
            response = requests.get(url)
            response.raise_for_status() 

            temp = response.json()['main']['temp']
            self.main_lbl_showtemperature.setText(str(temp) + " C°")

            weather_situation = response.json()['weather'][0]['description']
            self.main_lbl_showweathersituation.setText(weather_situation)

            weather_code = response.json()['weather'][0]['icon']
            self.pixmap = QPixmap()
            request = requests.get(f'https://openweathermap.org/img/wn/{weather_code}@2x.png')
            self.pixmap.loadFromData(request.content)
            self.main_lbl_showweathericon.setPixmap(self.pixmap)

            self.weather_records.update_one({"city_name": self.city_name},
                                            {"$set": {"temperature": temp,
                                                    "weather_situation": weather_situation,
                                                    "weather_code": weather_code}}, upsert=True)
            
        except requests.exceptions.HTTPError as err:
            if country_code == "BE":
                # Brüksel'in verileri kullanılacak.
                city_name = "Brussels"
                country_code = "BE"
                url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name},{country_code}&appid={API_key}&units=metric'
                response = requests.get(url)
                response.raise_for_status()

                temp = response.json()['main']['temp']
                self.main_lbl_showtemperature.setText(str(temp) + " C°")

                weather_situation = response.json()['weather'][0]['description']
                self.main_lbl_showweathersituation.setText(weather_situation)

                weather_code = response.json()['weather'][0]['icon']
                self.pixmap = QPixmap()
                request = requests.get(
                    f'https://openweathermap.org/img/wn/{weather_code}@2x.png')
                self.pixmap.loadFromData(request.content)
                self.main_lbl_showweathericon.setPixmap(self.pixmap)

                self.weather_records.update_one({"city_name": self.city_name},
                                                {"$set": {"temperature": temp,
                                                        "weather_situation": weather_situation,
                                                        "weather_code": weather_code}}, upsert=True)
            else:
                print(f"Error: {err}")
                self.main_lbl_searchwarning.setText("Something Went Wrong")

    def info(self):
        msg = QMessageBox()
        msg.setWindowTitle("Information")
        msg.setText("This application is created\non 28 March 2023\nby following developers:\n\nMelih YILMAZ\nMelike KAYA KARDIÇ\nTuba GÜMÜŞ")
        msg.setStyleSheet("background-color: rgba(92, 128, 154, 0.5);")
        x = msg. exec_()

    def exit(self):
        sys.exit()  

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = Main_Window()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(mainwindow)
    widget.show()
    try:
        sys.exit(app.exec_())
    except:
        print("Exiting")