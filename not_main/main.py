from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from pymongo import *
import sys, requests, certifi
from pymongo import MongoClient

from Ui_weather_main import *

#scrapy ayrı klasörde şehir isimleri, bölge/stateleri ve nüfusları

# connection = "mongodb+srv://tuba:1234@weatherapp.6zi3pge.mongodb.net/Configurations?retryWrites=true&w=majority"
# client = MongoClient(connection)
# client = MongoClient(connection, tlsCAFile=certifi.where())
# db = client.get_database ('WeatherApp')
# weather_records = db.weather
# countries_records = db.countries_data



class Main_Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Main_Window, self).__init__()
        self.setupUi(self)
        connection = "mongodb+srv://tuba:1234@weatherapp.6zi3pge.mongodb.net/Configurations?retryWrites=true&w=majority"
        # client = MongoClient(connection)
        client = MongoClient(connection, tlsCAFile=certifi.where())
        db = client.get_database ('WeatherApp')
        self.weather_records = db.weather
        self.countries_records = db.countries_data

        #self.BEupdate_city()
        """self.city_name = self.main_tbl_cities.item(0, 0).text()
        self.country_name = "BE"
        self.take_info()
        self.update_weather()"""

        self.main_btn_search.clicked.connect(self.search_city)
        self.main_btn_exit.clicked.connect(self.exit)

        self.main_btn_belgium.clicked.connect(self.BEupdate_city)
        #self.main_btn_belgium.clicked.connect(self.BEchange_colour)

        self.main_btn_germany.clicked.connect(self.DEupdate_city)
        #self.main_btn_germany.clicked.connect(self.DEchange_colour)

        self.main_btn_usa.clicked.connect(self.USupdate_city)
        #self.main_btn_usa.clicked.connect(self.USchange_colour)

        self.main_tbl_cities.itemClicked.connect(self.clicked_city)
        self.main_linedit_city.textChanged.connect(self.BEupdate_city)
        self.main_linedit_city.textChanged.connect(self.DEupdate_city)
        self.main_linedit_city.textChanged.connect(self.USupdate_city)
    
    def update_city_table(self, cities):
        row = 0
        self.main_tbl_cities.setRowCount(len(cities))
        for city in cities:
            self.main_tbl_cities.setItem(row, 0, QtWidgets.QTableWidgetItem(city))
            row += 1
            
    def clicked_city(self):
            indexes = []
            for selectionRange in self.main_tbl_cities.selectedRanges():
                indexes.extend(range(selectionRange.topRow(), selectionRange.bottomRow()+1))
                for i in indexes:
                    self.city_name = self.main_tbl_cities.item(i, 0).text()
                    self.take_info()
                    self.update_weather()
    
    def search_city(self):
        self.city_name = (self.main_linedit_city.text()).capitalize()
        try:
            # (self.city_name).capitalize()
            self.take_info()
            self.update_weather()
            self.main_lbl_searchwarning.hide()
        except:
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
 
    
    def BEupdate_city(self, text):
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
        self.main_btn_germany.setDefault(False)
        self.main_btn_usa.setDefault(False)
        self.main_btn_belgium.setDefault(True)

        if text:
            cities = [city["city_name"] for city in data_list if "city_name" in city and city["city_name"].lower().startswith(text.lower())]
            self.update_city_table(cities)
        else:
            self.update_city_table([city["city_name"] for city in data_list])

    def DEupdate_city(self, text):
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
        self.main_btn_belgium.setDefault(False)
        self.main_btn_usa.setDefault(False)
        self.main_btn_germany.setDefault(True)

        if text:
            cities = [city["city_name"] for city in data_list if "city_name" in city and city["city_name"].lower().startswith(text.lower())]
            self.update_city_table(cities)
        else:
            self.update_city_table([city["city_name"] for city in data_list])

    def USupdate_city(self, text):
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
        self.main_btn_belgium.setDefault(False)
        self.main_btn_germany.setDefault(False)
        self.main_btn_usa.setDefault(True)

        if text:
            cities = [city["city_name"] for city in data_list if "city_name" in city and city["city_name"].lower().startswith(text.lower())]
            self.update_city_table(cities)
        else:
            self.update_city_table([city["city_name"] for city in data_list])

    def update_weather(self):
        city_name = self.city_name
        country_code = self.country_name

        API_key = '38a18d9e8231ce64548938b0187511ce'
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name},{country_code}&appid={API_key}&units=metric'
        
        response = requests.get(url)
        temp = response.json()['main']['temp']
        self.main_lbl_showtemperature.setText(str(temp)+" C°")

        weather_situation = response.json()['weather'][0]['description']
        self.main_lbl_showweathersituation.setText(weather_situation)

        weather_code = response.json()['weather'][0]['icon']
        self.pixmap = QPixmap()
        request = requests.get(f'https://openweathermap.org/img/wn/{weather_code}@2x.png')
        self.pixmap.loadFromData(request.content)
        self.main_lbl_showweathericon.setPixmap(self.pixmap)

        # bu bilgilerden gerekli olanlar Mongoya atılıp oradan yazdırılacak
        #mongoya yazdırma için db.pymongo2.insert_one ({'name' : 'pymongo tutorial '}) veya find and update


        # mongodaki weather bilgisi updatei için: 

        # student updates = {'name': 'Nikhil'} 
        # records.update_one ({'roll_no': 123}, {'$set': student _updates})


        #mongodb ye veri yazdrima ###düzenlenecek!!!
#         #veri tabaninda collection olusturma
#         client = MongoClient()
#         db = client["WeatherApp"]
#         collection = db["weather"]
#         #hava durumunu Mongodb ye yazdirma
#         weather_data = {
#            "city_name" : self.city_name,
#            "temperature" : weather_situation['main']['temp'],
#            "weather_situation":weather_situation['weather'][0]['description'], 
#            "weather_code": weather_code['weather'][0]['icon']
# }
#         collection.insert_many(weather_data)

#         weather_data = {
#            "city_name" : self.city_name,
#            "temperature" :temp,
#            "weather_situation":weather_situation, 
#            "weather_code": weather_code 
# }
#         self.weather_records.insert_one(weather_data)


        self.weather_records.update_one({"city_name" : self.city_name},
                                        {"$set" :{"temperature" : temp,
                                                 "weather_situation": weather_situation, 
                                                 "weather_code": weather_code }},upsert=True)


    # def BEchange_colour(self)  :
    #     self.main_tbl_cities.setStyleSheet("background-color: rgb(255, 201, 255);")
        
    # def DEchange_colour(self):
    #     self.main_tbl_cities.setStyleSheet("background-color: rgb(153, 255, 255);")
        

    # def USchange_colour(self):
    #     self.main_tbl_cities.setStyleSheet("background-color: rgb(255, 255, 102);")
         


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