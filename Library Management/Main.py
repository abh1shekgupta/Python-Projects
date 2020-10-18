from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import *
import sys
import datetime
import sqlite3
from PyQt5.uic import loadUiType

ui, _ = loadUiType('library.ui')
login, _ = loadUiType('login.ui')


class Login(QtWidgets.QMainWindow, login):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent=parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.Handle_Login)
        self.Theme()

    def Theme(self):
        style = open('themes/AMOLED.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def Handle_Login(self):
        self.con = sqlite3.connect('Library.db')
        self.cur = self.con.cursor()

        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        self.cur.execute("select * from Users")
        data = self.cur.fetchall()
        if username != '' and password != '':
            for i in data:
                if username == i[1] and password == i[3]:
                    self.window2 = MainApp()
                    self.close()
                    self.window2.show()
                else:
                    self.label.setText(
                        'Make Sure you Entered ur Username & Password Correctly')
        else:
            self.label.setText('Field is Empty')
        self.con.close()


class MainApp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handle_ui_changes()
        self.Handle_Buttons()

        self.show_category()
        self.show_author()
        self.show_publisher()

        self.showCategoryCombobox()
        self.showAuthorCombobox()
        self.showPublisherCombobox()

        self.darkBlueTheme()

        self.ShowAllClient()
        self.showAllBook()

        self.showOperation()

    def Handle_ui_changes(self):
        self.hidingTheme()
        self.tabWidget.tabBar().setVisible(False)

    def Handle_Buttons(self):
        self.pushButton_theme.clicked.connect(self.showTheme)
        self.pushButton_HideTheme.clicked.connect(self.hidingTheme)

        self.pushButton_dayOp.clicked.connect(self.openDayOperation)
        self.pushButton_Book.clicked.connect(self.openBookTab)
        self.pushButton_client.clicked.connect(self.openClientTab)
        self.pushButton_User.clicked.connect(self.openUserTab)
        self.pushButton_setting.clicked.connect(self.openSettingTab)

        self.pushButton_AddNewBook.clicked.connect(self.AddNewBook)
        self.pushButton_9.clicked.connect(self.SearchBook)
        self.pushButton_8.clicked.connect(self.EditBook)
        self.pushButton_10.clicked.connect(self.deleteBook)

        self.pushButton_14.clicked.connect(self.Add_Category)
        self.pushButton_15.clicked.connect(self.Add_Author)
        self.pushButton_16.clicked.connect(self.Add_Publisher)

        self.pushButton_11.clicked.connect(self.AddNewUser)
        self.pushButton_12.clicked.connect(self.Login)
        self.pushButton_13.clicked.connect(self.EditUser)

        self.pushButton_17.clicked.connect(self.darkBlueTheme)
        self.pushButton_18.clicked.connect(self.darkTheme)
        self.pushButton_19.clicked.connect(self.ubuntuTheme)
        self.pushButton_21.clicked.connect(self.qDarkStyleTheme)
        self.pushButton_26.clicked.connect(self.lightTheme)
        self.pushButton_24.clicked.connect(self.materialDarkTheme)
        self.pushButton_22.clicked.connect(self.manjaroMixTheme)
        self.pushButton_25.clicked.connect(self.eleDarkTheme)
        self.pushButton_23.clicked.connect(self.consoleStyleTheme)
        self.pushButton_27.clicked.connect(self.aquaTheme)

        self.pushButton_AddNewclient.clicked.connect(self.AddNewClient)
        self.pushButton_28.clicked.connect(self.SearchClient)
        self.pushButton_20.clicked.connect(self.EditClient)
        self.pushButton_29.clicked.connect(self.DeleteClient)

        self.pushButton_6.clicked.connect(self.DayOperationHandle)

    def showTheme(self):
        self.groupBox_Theme.show()

    def hidingTheme(self):
        self.groupBox_Theme.hide()

    ################################
    ######## opening tabs ##########
    def openDayOperation(self):
        self.tabWidget.setCurrentIndex(0)

    def openBookTab(self):
        self.tabWidget.setCurrentIndex(1)

    def openClientTab(self):
        self.tabWidget.setCurrentIndex(2)

    def openUserTab(self):
        self.tabWidget.setCurrentIndex(3)

    def openSettingTab(self):
        self.tabWidget.setCurrentIndex(4)

    ##########################################
    ############ Day Operations  #############
    def DayOperationHandle(self):
        bookName = self.lineEdit.text()
        clientName = self.lineEdit_29.text()
        Type = self.comboBox.currentText()
        daysCount = self.comboBox_2.currentText()
        date_now = datetime.datetime.now()
        to_date = date_now + datetime.timedelta(days=int(daysCount))

        self.con = sqlite3.connect('Library.db')
        self.cur = self.con.cursor()
        if bookName != '' and clientName != '':
            self.cur.execute("insert into dayOperations(Book_name,Client,type,days,from_Date,to_Date) values('{}','{}','{}','{}','{}','{}');".format(
                bookName, clientName, Type, daysCount, str(date_now), str(to_date)))
            self.con.commit()
            self.statusBar().showMessage('New Operation Added..')
            self.con.close()
            self.showOperation()
        else:
            self.statusBar().showMessage('Empty Fields..')

    def showOperation(self):
        self.con = sqlite3.connect('Library.db')
        self.cur = self.con.cursor()

        self.cur.execute(
            "select  Book_name,Client,type,days,from_Date,to_Date from dayOperations")
        data = self.cur.fetchall()

        self.tableWidget.setRowCount(0)
        self.tableWidget.insertRow(0)
        for row, i in enumerate(data):
            for column, item in enumerate(i):
                self.tableWidget.setItem(row, column, QTableWidgetItem(item))
                column += 1
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)
        self.con.close()

    #################################
    ############ Books  #############

    def showAllBook(self):
        self.con = sqlite3.connect('Library.db')
        self.cur = self.con.cursor()
        self.cur.execute(
            "select Book_Code,Book_name,Book_Description,Book_Category,Book_Author,Book_Publisher,Book_Price from Book order by Book_Code")
        data = self.cur.fetchall()
        self.tableWidget_5.setRowCount(0)
        self.tableWidget_5.insertRow(0)
        for row, i in enumerate(data):
            for column, item in enumerate(i):
                self.tableWidget_5.setItem(
                    row, column, QTableWidgetItem(str(item)))
                column += 1
            row_position = self.tableWidget_5.rowCount()
            self.tableWidget_5.insertRow(row_position)
        self.con.close()

    def AddNewBook(self):
        self.con = sqlite3.connect('Library.db')
        self.cur = self.con.cursor()

        bookTitle = self.lineEdit_3.text()
        bookDesc = self.textEdit.toPlainText()
        bookCode = self.lineEdit_5.text()
        bookCategory = self.comboBox_3.currentText()
        bookAuthor = self.comboBox_4.currentText()
        bookPublisher = self.comboBox_5.currentText()
        bookPrice = self.lineEdit_4.text()

        self.cur.execute(
            "insert into Book(Book_Name,Book_Description,Book_Code,Book_Category,Book_Author,Book_Publisher,Book_Price) values('{}','{}','{}','{}','{}','{}',{});"
                .format(bookTitle, bookDesc, bookCode, bookCategory, bookAuthor, bookPublisher, bookPrice))
        self.con.commit()
        self.statusBar().showMessage('New Book Added')

        self.lineEdit_3.setText('')
        self.textEdit.setPlainText('')
        self.lineEdit_5.setText('')
        self.comboBox_3.setCurrentIndex(0)
        self.comboBox_4.setCurrentIndex(0)
        self.comboBox_5.setCurrentIndex(0)
        self.lineEdit_4.setText('')
        self.con.close()
        self.showAllBook()

    def SearchBook(self):
        self.con = sqlite3.connect('Library.db')
        self.cur = self.con.cursor()
        bookCode = self.lineEdit_9.text()

        sql = "select * from Book where Book_Code = '{}';".format(bookCode)
        self.cur.execute(sql)
        data = self.cur.fetchone()

        self.lineEdit_8.setText(data[1])
        self.textEdit_2.setPlainText(data[2])
        self.lineEdit_6.setText(data[3])
        self.comboBox_8.setCurrentText(data[4])
        self.comboBox_7.setCurrentText(data[5])
        self.comboBox_6.setCurrentText(data[6])
        self.lineEdit_7.setText(str(data[7]))

        self.con.close()
        self.showAllBook()

    def EditBook(self):
        self.con = sqlite3.connect('Library.db')
        self.cur = self.con.cursor()

        bookTitle = self.lineEdit_8.text()
        bookDesc = self.textEdit_2.toPlainText()
        bookCode = self.lineEdit_6.text()
        bookCategory = self.comboBox_8.currentText()
        bookAuthor = self.comboBox_7.currentText()
        bookPublisher = self.comboBox_6.currentText()
        bookPrice = self.lineEdit_7.text()

        searchBookTitle = self.lineEdit_9.text()
        self.cur.execute(
            "update Book set Book_Name='{}',Book_Description='{}',Book_Code='{}',Book_Category='{}',Book_Author='{}',Book_Publisher='{}',Book_Price='{}' where Book_Name='{}';".format(bookTitle, bookDesc, bookCode, bookCategory, bookAuthor, bookPublisher, bookPrice, searchBookTitle))
        self.con.commit()
        self.statusBar().showMessage('Book Updated')

        self.con.close()
        self.showAllBook()

    def deleteBook(self):
        self.con = sqlite3.connect('Library.db')
        self.cur = self.con.cursor()

        bookCode = self.lineEdit_9.text()
        warning = QMessageBox.warning(
            self, 'Delete Book', 'Are you sure u wanna delete this book', QMessageBox.Yes | QMessageBox.No)
        if warning == QMessageBox.Yes:
            self.cur.execute(
                "delete from Book where Book_Code='{}'".format(bookCode))
            self.con.commit()
            self.statusBar().showMessage('Book Deleted')
            self.con.close()

        self.showAllBook()

    ################################
    ########### Clients ############
    def ShowAllClient(self):
        self.con = sqlite3.connect('Library.db')
        self.cur = self.con.cursor()
        self.cur.execute("select Name,Email,National_id from Client")
        data = self.cur.fetchall()
        self.tableWidget_6.setRowCount(0)
        self.tableWidget_6.insertRow(0)
        for row, i in enumerate(data):
            for column, item in enumerate(i):
                self.tableWidget_6.setItem(
                    row, column, QTableWidgetItem(str(item)))
                column += 1
            row_position = self.tableWidget_6.rowCount()
            self.tableWidget_6.insertRow(row_position)
        self.con.close()

    def AddNewClient(self):
        name = self.lineEdit_22.text()
        email = self.lineEdit_23.text()
        Nat_id = self.lineEdit_24.text()

        self.con = sqlite3.connect('Library.db')
        self.cur = self.con.cursor()

        self.cur.execute(
            "insert into Client(Name,Email,National_id) values('{}','{}','{}');".format(name, email, Nat_id))
        self.con.commit()
        self.statusBar().showMessage('New Client Added')
        self.ShowAllClient()
        self.con.close()

    def SearchClient(self):
        Nat_id = self.lineEdit_28.text()
        self.con = sqlite3.connect('Library.db')
        self.cur = self.con.cursor()
        self.cur.execute(
            "select * from Client where National_id='{}'".format(Nat_id))
        data = self.cur.fetchone()

        self.lineEdit_25.setText(data[1])
        self.lineEdit_26.setText(data[2])
        self.lineEdit_27.setText(str(data[3]))
        self.ShowAllClient()
        self.con.close()

    def EditClient(self):
        OriginalNat_id = self.lineEdit_28.text()
        name = self.lineEdit_25.text()
        email = self.lineEdit_26.text()
        newNat_id = self.lineEdit_27.text()
        self.con = sqlite3.connect('Library.db')
        self.cur = self.con.cursor()
        self.cur.execute(
            "update Client set Name='{}',Email='{}',National_id='{}' where National_id='{}'".format(name, email, newNat_id, OriginalNat_id))
        self.con.commit()
        self.statusBar().showMessage('Client Data Updated..')
        self.ShowAllClient()
        self.con.close()

    def DeleteClient(self):
        Nat_id = self.lineEdit_28.text()

        warn = QMessageBox.warning(
            self, "Delete Client", "Are u sure u wanna delete this client", QMessageBox.Yes | QMessageBox.No)
        if warn == QMessageBox.Yes:
            self.con = sqlite3.connect('Library.db')
            self.cur = self.con.cursor()
            self.cur.execute(
                "delete from Client where National_id='{}'".format(Nat_id))
            self.con.commit()
            self.statusBar().showMessage('Client Data Deleted..')
            self.ShowAllClient()
            self.con.close()

    ################################
    ############ Users #############

    def AddNewUser(self):
        self.con = sqlite3.connect('Library.db')
        self.cur = self.con.cursor()

        username = self.lineEdit_2.text()
        email = self.lineEdit_10.text()
        password = self.lineEdit_11.text()
        password2 = self.lineEdit_12.text()
        if password == password2:
            self.cur.execute("insert into Users(user_name,user_email,user_password) values('{}','{}','{}')".format(
                username, email, password))
            self.con.commit()
            self.statusBar().showMessage('New User Added')
            self.con.close()
        else:
            self.label_19.setText('Please add Valid Password Twice')

    def Login(self):
        self.con = sqlite3.connect('Library.db')
        self.cur = self.con.cursor()

        username = self.lineEdit_14.text()
        password = self.lineEdit_13.text()

        self.cur.execute("select * from Users")
        data = self.cur.fetchall()
        for i in data:
            if username == i[1] and password == i[3]:
                self.statusBar().showMessage('Valid User')
                self.groupBox_3.setEnabled(True)

                self.lineEdit_18.setText(i[1])
                self.lineEdit_15.setText(i[2])
                self.lineEdit_16.setText(i[3])
        self.con.close()

    def EditUser(self):
        usernameSearch = self.lineEdit_14.text()
        username = self.lineEdit_18.text()
        email = self.lineEdit_15.text()
        password = self.lineEdit_16.text()
        password2 = self.lineEdit_17.text()

        if password == password2:
            self.con = sqlite3.connect('Library.db')
            self.cur = self.con.cursor()

            self.cur.execute("update Users set user_name='{}',user_email='{}',user_password='{}' where user_name='{}'".format(
                username, email, password, usernameSearch))
            self.con.commit()
            self.statusBar().showMessage('User Data Updated Successfully..')
            self.con.close()
        else:
            self.statusBar().showMessage('Make sure to enter password correctly')

    ################################
    ########## Settings ############

    def Add_Category(self):
        self.con = sqlite3.connect('Library.db')

        categoryName = str(self.lineEdit_19.text())
        self.con.execute(
            "insert into Category(category_name) values('{}');".format(categoryName))
        self.con.commit()
        self.statusBar().showMessage('New Category Added')
        self.lineEdit_19.setText('')
        self.show_category()
        self.showCategoryCombobox()
        self.con.close()

    def show_category(self):
        self.con = sqlite3.connect('Library.db')
        self.cur = self.con.cursor()
        self.cur.execute("select category_name from Category")
        data = self.cur.fetchall()
        if data:
            self.tableWidget_2.setRowCount(0)  # clear table each time
            self.tableWidget_2.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget_2.setItem(
                        row, column, QTableWidgetItem(str(item)))
                    column += 1
                row_position = self.tableWidget_2.rowCount()
                self.tableWidget_2.insertRow(row_position)
        self.con.close()

    def Add_Author(self):
        self.con = sqlite3.connect('Library.db')

        authorName = str(self.lineEdit_20.text())
        self.con.execute(
            "insert into authors(author_name) values('{}');".format(authorName))
        self.con.commit()
        self.statusBar().showMessage('New Author Added')
        self.lineEdit_20.setText('')
        self.show_author()
        self.showAuthorCombobox()
        self.con.close()

    def show_author(self):
        self.con = sqlite3.connect('Library.db')
        self.cur = self.con.cursor()
        self.cur.execute("select author_name from authors")
        data = self.cur.fetchall()
        if data:
            self.tableWidget_3.setRowCount(0)  # clear table each time
            self.tableWidget_3.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget_3.setItem(
                        row, column, QTableWidgetItem(str(item)))
                    column += 1
                row_position = self.tableWidget_3.rowCount()
                self.tableWidget_3.insertRow(row_position)
        self.con.close()

    def Add_Publisher(self):
        self.con = sqlite3.connect('Library.db')

        publisherName = str(self.lineEdit_21.text())
        self.con.execute(
            "insert into publisher(publisher_name) values('{}');".format(publisherName))
        self.con.commit()
        self.statusBar().showMessage('New Publisher Added')
        self.lineEdit_21.setText('')
        self.show_publisher()
        self.showPublisherCombobox()
        self.con.close()

    def show_publisher(self):
        self.con = sqlite3.connect('Library.db')
        self.cur = self.con.cursor()
        self.cur.execute("select publisher_name from publisher")
        data = self.cur.fetchall()
        if data:
            self.tableWidget_4.setRowCount(0)  # clear table each time
            self.tableWidget_4.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget_4.setItem(
                        row, column, QTableWidgetItem(str(item)))
                    column += 1
                row_position = self.tableWidget_4.rowCount()
                self.tableWidget_4.insertRow(row_position)
        self.con.close()

    ###################################################
    ############ show settings data in UI #############
    def showCategoryCombobox(self):
        self.con = sqlite3.connect('Library.db')
        self.cur = self.con.cursor()
        self.cur.execute("select category_name from Category")
        data = self.cur.fetchall()
        self.comboBox_3.clear()

        for i in data:
            self.comboBox_3.addItem(i[0])
            self.comboBox_8.addItem(i[0])
        self.con.close()

    def showAuthorCombobox(self):
        self.con = sqlite3.connect('Library.db')
        self.cur = self.con.cursor()
        self.cur.execute("select author_name from authors")
        data = self.cur.fetchall()
        self.comboBox_4.clear()

        for i in data:
            self.comboBox_4.addItem(i[0])
            self.comboBox_7.addItem(i[0])
        self.con.close()

    def showPublisherCombobox(self):
        self.con = sqlite3.connect('Library.db')
        self.cur = self.con.cursor()
        self.cur.execute("select publisher_name from publisher")
        data = self.cur.fetchall()
        self.comboBox_5.clear()

        for i in data:
            self.comboBox_5.addItem(i[0])
            self.comboBox_6.addItem(i[0])
        self.con.close()

    ################################
    ########## UI Themes ###########
    def darkBlueTheme(self):
        style = open('themes/darkBlue.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def darkTheme(self):
        style = open('themes/dark.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def ubuntuTheme(self):
        style = open('themes/Ubuntu.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def qDarkStyleTheme(self):
        style = open('themes/qDarkStyle.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def lightTheme(self):
        style = open('themes/light.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def materialDarkTheme(self):
        style = open('themes/MaterialDark.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def manjaroMixTheme(self):
        style = open('themes/ManjaroMix.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def eleDarkTheme(self):
        style = open('themes/ElegantDark.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def consoleStyleTheme(self):
        style = open('themes/ConsoleStyle.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def aquaTheme(self):
        style = open('themes/aqua.css', 'r')
        style = style.read()
        self.setStyleSheet(style)


def main():
    app = QApplication(sys.argv)
    window = Login()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
