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

        # connection with the Mongo DB
        try:
            connection = "mongodb+srv://melike:1234@weatherapp.xzog7un.mongodb.net/?retryWrites=true&w=majority"
            client = MongoClient(connection, tlsCAFile=certifi.where())
            db = client.get_database ('WeatherApp')
            self.weather_records = db.weather           # the collection where the wheather data is held
            self.countries_records = db.countries_data  # the collection where the country data is held
        except :
            self.main_lbl_searchwarning.setText("No internet connection!")

        # to fill the first data when the app is started
        try:
            self.BEupdate_city()
            self.city_name = self.main_tbl_cities.item(0, 0).text()
            self.country_name = "BE"
            self.take_info()
            self.update_weather()
        except:
            self.main_lbl_showcityname.setText("Antwerp")
            self.main_lbl_showtemperature.setText("i wish C°")
            self.main_lbl_showweathersituation.setText("sunny we hope")
            self.main_lbl_showweathericon.setText(":)")
            self.main_lbl_showcountry.setText("Belgium")
            self.main_lbl_showstate.setText("Flanders")
            self.main_lbl_showpopulation.setText("529,247")

        try: # try for working without connection
            self.main_btn_search.clicked.connect(self.search_city)
            self.main_btn_exit.clicked.connect(self.exit)

            self.main_btn_belgium.clicked.connect(self.BEupdate_city)
            self.main_btn_germany.clicked.connect(self.DEupdate_city)
            self.main_btn_usa.clicked.connect(self.USupdate_city)
            self.main_tbl_cities.itemClicked.connect(self.clicked_city)

            self.main_btn_info.clicked.connect(self.info)
            self.deneme()
        except:
            pass
    
    def clicked_city(self):
        """A method for updating data chosen from the table"""
        indexes = []
        for selectionRange in self.main_tbl_cities.selectedRanges():
            indexes.extend(range(selectionRange.topRow(), selectionRange.bottomRow()+1)) # adding the indexes into a list to stroll in the table widget
            for i in indexes:
                self.city_name = self.main_tbl_cities.item(i, 0).text()  # to take the city_name when a row is clicked in the table widget
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
        except requests.exceptions.ConnectionError:
            self.main_lbl_searchwarning.setText("No internet connection!")

    def info(self):
        msg = QMessageBox()
        msg.setWindowTitle("Information")
        msg.setText("This application is created\non 28 March 2023\nby following developers:\n\nMelih YILMAZ\nMelike KAYA KARDIÇ\nTuba GÜMÜŞ")
        msg.setStyleSheet("background-color: rgb(92, 128, 154);")
        msg.setWindowOpacity(0.95)
        x = msg. exec_()

    def exit(self):
        sys.exit()  

    def deneme(self):
        self.controls = QWidget()  # Controls container widget.
        self.controlsLayout = QVBoxLayout()   # Controls container layout.
        # List of names, widgets are stored in a dictionary by these keys.

        search_term = self.main_linedit_city.text().lower()
        query = {"city_name": {"$regex": "^" + search_term, "$options": "i"}}
        reader = self.countries_records.find(query, {'city_name': 1})
        self.data_list = [data['city_name'] for data in reader]

        self.widgets = []
        # Iterate the names, creating a new OnOffWidget for
        # each one, adding it to the layout and
        # and storing a reference in the self.widgets dict
        for name in self.data_list:
            item = OnOffWidget(name)
            self.controlsLayout.addWidget(item)
            self.widgets.append(item)
        spacer = QSpacerItem(1, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.controlsLayout.addItem(spacer)
        self.controls.setLayout(self.controlsLayout)
        # Scroll Area Properties.
        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.controls)
        # Search bar.
        # self.mainscreen.edt_search = QLineEdit()
        self.main_linedit_city.textChanged.connect(self.update_display)
        # Adding Completer.
        self.completer = QCompleter(self.data_list)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.main_linedit_city.setCompleter(self.completer)
        # Add the items to VBoxLayout (applied to container widget)
        # which encompasses the whole window.
        containerLayout = QVBoxLayout()
        containerLayout.addWidget(self.main_linedit_city)
        containerLayout.addWidget(self.scroll)
        # container.setLayout(containerLayout)
        # container.setGeometry(QtCore.QRect(500, 60, 361, 31))
        # self.setCentralWidget(container)
    def update_display(self):
        search_term = self.main_linedit_city.text().lower()
        city_names = self.data_list
        matches = [city for city in city_names if search_term in city.lower()]
        model = QStringListModel()
        model.setStringList(matches)
        self.completer.setModel(model)

class OnOffWidget(QWidget):
    def __init__(self, name):
        super(OnOffWidget, self).__init__()
        self.name = name
        self.is_on = False


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