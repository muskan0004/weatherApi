import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout)

from PyQt5.QtCore import Qt  # this will help with alignments


class wapp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_l = QLabel("Enter city name", self)
        self.cinput = QLineEdit(self)  # this will create a text input box
        self.wbut = QPushButton("Get Weather", self)
        self.templabel = QLabel(self)  # 30 degree c is just an placeholderfj
        self.emoji = QLabel(self)
        self.desc = QLabel(self)
        # if you run now , all the above widgets will be stacking on the top left hand corner; so to avoid that we design
        # a layout
        self.ui()  #  we'll have to call it here or the above mentioned problem will be not solved

    def ui(self):
        self.setWindowTitle("Weather APP")

        # vertically aligning
        vb = QVBoxLayout()
        vb.addWidget(self.city_l)
        vb.addWidget(self.cinput)
        vb.addWidget(self.wbut)
        vb.addWidget(self.templabel)
        vb.addWidget(self.emoji)
        vb.addWidget(self.desc)

        self.setLayout(vb)
        #  horizontal aligning
        self.city_l.setAlignment(Qt.AlignCenter)
        self.cinput.setAlignment(Qt.AlignCenter)
        self.templabel.setAlignment(Qt.AlignCenter)
        self.emoji.setAlignment(Qt.AlignCenter)
        self.desc.setAlignment(Qt.AlignCenter)

        # we tone down the ugliness of it using css
        self.city_l.setObjectName("city_l")
        self.cinput.setObjectName("cinput")
        self.wbut.setObjectName("wbut")
        self.templabel.setObjectName("templabel")
        self.emoji.setObjectName("emoji")
        self.desc.setObjectName("desc")

        self.setStyleSheet("""
        QLabel, QPushButton{
             font-family:  calibri;
        }
        QLabel#city_l{
             font-size: 40px;
             font-style: italic;
        }
        QLineEdit#cinput{
             font-size:40px;
        }
        QPushButton#wbut{
             font-size: 30px;
             font-weight: bold;
        }
        QLabel#templabel{
             font-size: 75px;
             
        }  
        QLabel#emoji{
             font-size: 100px;
             font-family: Segoe UI emoji;
        }
        QLabel#desc{
             font-size: 50px;
        }    
                     """)
        self.wbut.clicked.connect(self.getweather)

    def getweather(self):

        global response
        apikey = "use_your_own"
        city = self.cinput.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={apikey}"
        try:
            response = requests.get(url)
            data = response.json()
            response.raise_for_status()
            if data['cod'] == 200:
                self.dweather(data)

        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.derror("Check your input")
                case 401:
                    self.derror("unauthorized; Invalid API key")
                case 403:
                    self.derror("Forbidden \n Access Denied")
                case 404:
                    self.derror("Not Found \n City not found")
                case 500:
                    self.derror("Internal Server Error; Try again later")
                case 502:
                    self.derror("bad gateway \nInvalid response from the server")

                case 503:
                    self.derror("Service Unavailabe \n Server is down")
                case 504:
                    self.derror("Gateway Timeout\n no response from the server")
                case _:
                    self.derror(f"HTTP ERROR occurred {http_error}")
        except requests.exceptions.ConnectionError:
            self.derror("Connection Error: \n CHeck your internet connection")
        except requests.exceptions.Timeout:
            self.derror("Time out error: \n The request timed out")
        except requests.exceptions.TooManyRedirects:
            self.derror("TOO MANY REQUESTS\n")
        except requests.exceptions.RequestException as req_error:
            self.derror(f"Request Error: \n{req_error}")

    def derror(self, message):
        self.templabel.setStyleSheet("font-size: 30px;")
        self.templabel.setText(message)
        self.emoji.clear()
        self.desc.clear()

    def dweather(self, data):
        self.templabel.setStyleSheet("font-size: 75px;")
        tempk = data["main"]["temp"]  # here we are accessing the main key and its values
        tempf = (tempk * 9 / 5) - 459.67
        weather_id = data["weather"][0]["id"]
        wdesc = data["weather"][0]["description"]

        self.templabel.setText(f"{tempf:.0f}°F")
        self.emoji.setText(self.wemoji(weather_id))
        self.desc.setText(wdesc)

    @staticmethod
    def wemoji(weather_id):
        if 200 <= weather_id <= 232:
            return "⛈️"
        elif 300 <= weather_id <= 321:
            return "🌦️"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id <= 622:
            return "❄️"
        elif 701 <= weather_id <= 741:
            return "🌫️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "☀️"
        elif 801 <= weather_id <= 804:
            return "☁️"
        else:
            return " "


if __name__ == "__main__":
    app = QApplication(sys.argv)
    wa = wapp()
    wa.show()
    sys.exit(app.exec_())
