from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from pymongo import *
import sys, requests, certifi

from Ui_weather_main import *

#scrapy ayrı klasörde şehir isimleri, bölge/stateleri ve nüfusları

connection = "mongodb+srv://tuba:1234@weatherapp.6zi3pge.mongodb.net/Configurations?retryWrites=true&w=majority"
client = MongoClient(connection)
client = MongoClient(connection, tlsCAFile=certifi.where())
db = client.get_database ('WeatherApp')
records = db.weather

# records.insert_many(......buraya liste içine {a:ajksf} şeklinde giriş jsondan)


class Main_Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Main_Window, self).__init__()
        self.setupUi(self)
        # self.main = Main_Window()

        self.main_btn_search.clicked.connect(self.search)
        self.main_btn_exit.clicked.connect(self.exit)

    

    def update_city(self):
        # mongodb den şehir çek

        pass

    def search(self):
        city_name = "Seraing"
        country_code = "be"
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


        # mongodaki weather bilgisi updatei için: 

        # student updates = {'name': 'Nikhil'} 
        # records.update_one ({'roll_no': 123}, {'$set': student _updates})

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