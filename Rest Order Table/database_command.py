import sqlite3


def createdb():
    try:
        con = sqlite3.connect('order history.db')
        con.close()
    except:
        print('error occur---During creating database---')


def createTable():
    try:
        con = sqlite3.connect('order history.db')
        table = "create table Order_History(SrNo integer primary key autoincrement,Reference_No integer,Cost_of_Meal real,VAT real, Service_charge real,Total_Cost real,Date_Time text,Payment_Mode text);"
        con.execute(table)
        con.close()
    except Exception as e:
        print(e)


def InsertData(RefNo, COM, Vat, SC, TC, cDate, payMode):
    con = sqlite3.connect('order history.db')
    insert = "insert into Order_History(Reference_No,Cost_of_Meal,VAT,Service_charge,Total_Cost,Date_Time,Payment_Mode) values({},{},{},{},{},'{}','{}');".format(
        RefNo, COM, Vat, SC, TC, cDate, payMode)
    con.execute(insert)
    con.commit()
    con.close()


createdb()
createTable()
