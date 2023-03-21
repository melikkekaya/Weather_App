from PyQt5.QtWidgets import *
import sys

from Ui_weather_main import *

#scrapy ayrı klasörde şehir isimleri, bölge/stateleri ve nüfusları


class Main_Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Main_Window, self).__init__()
        self.setupUi(self)
        self.main_btn_search.clicked.connect(self.search)
        self.main_btn_exit.clicked.connect(self.exit)

    

    def update_city():
        # mongodb den şehir çek

        pass

    def search():
        # api
        # 
        pass



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