from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys, requests

from Ui_weather_main import *

#scrapy ayrı klasörde şehir isimleri, bölge/stateleri ve nüfusları


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
        # print(response)
        result = response.json()
        temp = response.json()['main']['temp']
        self.main_lbl_showtemperature.setText(str(temp)+" C°")
        # weather = response.json()['weather'][0]
        weather_code = response.json()['weather'][0]['icon']
        

        # new_url = 'https://openweathermap.org/img/wn/10d@2x.png'
        # image = requests.get(new_url)

        # self.main_lbl_showweathericon.setPicture(image)
        # pixmap = QPixmap('02n@2x.png')
        # self.main_lbl_showweathericon.setPixmap(pixmap)


        # url2 = f'https://openweathermap.org/img/wn/{weather_code}@2x.png'
        # response2 = requests.get(url2)
        # if response2.status_code == 200:
        #     with open(f'sample{weather_code}.jpg', 'wb') as f:
        #         f.write(response2.content)
        # pixmap = QPixmap(f'sample{weather_code}.jpg' + weather_code + ".jpg")
        # pixmap = QPixmap("http://openweathermap.org/img/wn/" + weather_code + "@2x.png");
        # self.main_lbl_showweathericon.setPixmap(pixmap)

        self.pixmap = QPixmap()
        request = requests.get(f'https://openweathermap.org/img/wn/{weather_code}@2x.png')
        self.pixmap.loadFromData(request.content)
        self.main_lbl_showweathericon.setPixmap(self.pixmap)
        
        
    

        # bu bilgilerden gerekli olanlar Mongoya atılıp oradan yazdırılacak


        # print(f"\n1 {first} is {result} {second} on {day}/{month}/{year}")
        # api
        # 
        



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
    


   
# # HIDE PROGRESSBAR AND MESSAGES CONTAINER BY DEFAULT
# self.ui.progressBar.setVisible(False);
# self.ui.message_frame.hide ()