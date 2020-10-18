import requests
import sys
import sqlite3
import datetime
from PyQt5 import QtWidgets, uic


def checkWeather():
    window.label_6.setText('')
    cityName = window.lineEdit.text()
    url = "https://api.openweathermap.org/data/2.5/weather?q=" + \
        cityName+"&appid=##############"     ''' Here #### these are replace with API key'''
    try:
        result = requests.get(url)
        x = result.json()
        temp = (int(x['main']['temp']) - 273.15)
        FinalTemp = '{:04.2f}'.format(temp)
        humidity = x['main']['humidity']
        pressure = x['main']['pressure']
        CurrentTime = str(datetime.datetime.now())[:-7]

        window.label_7.setText(FinalTemp+' °C')
        window.label_8.setText(str(humidity)+" %")
        window.label_9.setText(str(pressure)+" mmHg")

        con = sqlite3.connect('RecentSearchesDatabase.db')
        con.execute(
            "insert into Recent_Searches(city,temperature,humidity,pressure,Date_Time) values('{}','{}','{}','{}','{}')".format(cityName, (FinalTemp+' °C'), (str(humidity)+" %"), (str(pressure)+" mmHg"), CurrentTime))
        con.commit()
        con.close()
    except:
        window.label_7.setText('')
        window.label_8.setText('')
        window.label_9.setText('')
        window.label_6.setText(
            'Unable to find the information for the given city')


def recentSearches():
    searches.show()
    con = sqlite3.connect('RecentSearchesDatabase.db')
    cur = con.cursor()
    cur.execute(
        "select city,temperature,humidity,pressure,Date_Time from Recent_Searches")
    data = cur.fetchall()
    searches.tableWidget.insertRow(0)
    searches.tableWidget.setRowCount(0)
    searches.tableWidget.insertRow(0)
    for row, i in enumerate(data):
        for column, j in enumerate(i):
            searches.tableWidget.setItem(
                row, column, QtWidgets.QTableWidgetItem(str(j)))
            column += 1
        rowPosition = searches.tableWidget.rowCount()
        searches.tableWidget.insertRow(rowPosition)
    con.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    style = open('themes/AMOLED.css', 'r')
    style = style.read()
    app.setStyleSheet(style)
    window = uic.loadUi('Main.ui')
    searches = uic.loadUi('Searches.ui')
    window.show()
    window.pushButton.clicked.connect(checkWeather)
    window.pushButton_2.clicked.connect(recentSearches)
    sys.exit(app.exec_())
