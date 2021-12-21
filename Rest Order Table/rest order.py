import sys
import time
import random
import playsound
import math
import datetime
import database_command as dc
from PyQt5 import QtWidgets, uic


def closeIntro():
    intro.close()
    menu.show()


def openPList():
    price_list.show()


def CalTotal():
    global serviceCharge
    serviceCharge = 0
    price = [8, 120, 90, 130, 70, 35, 550, 700, 200, 300, 70, 7, 100, 12]
    Purchase_list = []
    if menu.ipRoti.text() == '':
        Purchase_list.append(0)
    else:
        Purchase_list.append(int(menu.ipRoti.text()))
        serviceCharge += 5

    if menu.ipDaal.text() == '':
        Purchase_list.append(0)
    else:
        Purchase_list.append(int(menu.ipDaal.text()))
        serviceCharge += 5

    if menu.ipAloo.text() == '':
        Purchase_list.append(0)
    else:
        Purchase_list.append(int(menu.ipAloo.text()))
        serviceCharge += 5

    if menu.ipPaneer.text() == '':
        Purchase_list.append(0)
    else:
        Purchase_list.append(int(menu.ipPaneer.text()))
        serviceCharge += 5

    if menu.ipRice.text() == '':
        Purchase_list.append(0)
    else:
        Purchase_list.append(int(menu.ipRice.text()))
        serviceCharge += 5

    if menu.ipNaan.text() == '':
        Purchase_list.append(0)
    else:
        Purchase_list.append(int(menu.ipNaan.text()))
        serviceCharge += 5

    if menu.ipChicken.text() == '':
        Purchase_list.append(0)
    else:
        Purchase_list.append(int(menu.ipChicken.text()))
        serviceCharge += 5

    if menu.ipMutton.text() == '':
        Purchase_list.append(0)
    else:
        Purchase_list.append(int(menu.ipMutton.text()))
        serviceCharge += 5

    if menu.ipKebab.text() == '':
        Purchase_list.append(0)
    else:
        Purchase_list.append(int(menu.ipKebab.text()))
        serviceCharge += 5

    if menu.ipFish.text() == '':
        Purchase_list.append(0)
    else:
        Purchase_list.append(int(menu.ipFish.text()))
        serviceCharge += 5

    if menu.ipCold.text() == '':
        Purchase_list.append(0)
    else:
        Purchase_list.append(int(menu.ipCold.text()))
        serviceCharge += 5

    if menu.ipTea.text() == '':
        Purchase_list.append(0)
    else:
        Purchase_list.append(int(menu.ipTea.text()))
        serviceCharge += 5

    if menu.ipEnergy.text() == '':
        Purchase_list.append(0)
    else:
        Purchase_list.append(int(menu.ipEnergy.text()))
        serviceCharge += 5

    if menu.ipCoffee.text() == '':
        Purchase_list.append(0)
    else:
        Purchase_list.append(int(menu.ipCoffee.text()))
        serviceCharge += 5

    RefNo()
    global CostOfMeal
    CostOfMeal_list = [Purchase_list[i]*price[i] for i in range(len(price))]
    CostOfMeal = sum(CostOfMeal_list)
    menu.opCOM.setText('Rs.'+str(CostOfMeal))

    global vat
    vat = CostOfMeal*0.05
    menu.opVAT.setText('Rs.'+str(vat))

    menu.opSC.setText('Rs.'+str(serviceCharge))

    totalcost = CostOfMeal+vat+serviceCharge
    global totalcostGlobal
    totalcostGlobal = totalcost
    menu.opTotal.setText('Rs.'+str(totalcost))


def RefNo():
    global ref_state
    if ref_state == 1:
        global refNo
        refNo = random.randint(1234567, 9876543)
        menu.opRef.setText(str(refNo))
        ref_state = 0


def resetAll():
    menu.ipRoti.setText('')
    menu.ipDaal.setText('')
    menu.ipAloo.setText('')
    menu.ipPaneer.setText('')
    menu.ipRice.setText('')
    menu.ipNaan.setText('')
    menu.ipChicken.setText('')
    menu.ipMutton.setText('')
    menu.ipKebab.setText('')
    menu.ipFish.setText('')
    menu.ipCold.setText('')
    menu.ipTea.setText('')
    menu.ipEnergy.setText('')
    menu.ipCoffee.setText('')
    menu.opRef.setText('')
    menu.opCOM.setText('')
    menu.opSC.setText('')
    menu.opVAT.setText('')
    menu.opTotal.setText('')
    global ref_state
    ref_state = 1


def quitall():
    sys.exit()


def choosePayment():
    ch_pay.show()


def qrcode_payment():
    global totalcostGlobal
    ch_pay.close()
    qr.show()
    qr.totalPayment.setText('Rs. '+str(totalcostGlobal))


def cash_payment():
    global totalcostGlobal
    if totalcostGlobal != 0:
        ch_pay.close()
        cash.show()
        cash.totalPayment.setText('Rs. '+str(totalcostGlobal))
        cash.payMade.setText('')
        cash.balance.setText('')
        cash.paymentDone.clicked.connect(cashPayDone)
    else:
        totalcostGlobal = 0
        pass  # If No order is given & cash paymnt is made


def cashPayDone():
    global totalcostGlobal
    paid = int(cash.payMade.text())
    cash.balance.setText('Rs. '+str(math.floor(paid)-totalcostGlobal))
    global refNo, CostOfMeal, vat, serviceCharge
    CurrentDate = str(datetime.datetime.now())
    dc.InsertData(refNo, CostOfMeal, vat, serviceCharge,
                  totalcostGlobal, CurrentDate, "Cash")
    # time.sleep(2)
    playsound.playsound('audio.mp3', True)
    # cash.close()


def Payment_done():
    playsound.playsound('audio.mp3', True)
    CurrentDate = str(datetime.datetime.now())
    global refNo, CostOfMeal, vat, serviceCharge, totalcostGlobal
    dc.InsertData(refNo, CostOfMeal, vat, serviceCharge,
                  totalcostGlobal, CurrentDate, "QrCode")
    qr.close()


if __name__ == "__main__":
    global vat, serviceCharge, CostOfMeal, ref_state, totalcostGlobal, refNo
    ref_state = 1
    try:
        dc.createdb()
    except:
        pass
    try:
        dc.createTable()
    except:
        pass
    app = QtWidgets.QApplication([])
    intro = uic.loadUi('intro.ui')
    menu = uic.loadUi('mainMenu.ui')
    price_list = uic.loadUi('PriceList.ui')
    ch_pay = uic.loadUi('payment.ui')
    qr = uic.loadUi('qrscan.ui')
    cash = uic.loadUi('cash.ui')
    intro.show()
    intro.introCont.clicked.connect(closeIntro)
    menu.priceList.clicked.connect(openPList)
    menu.total.clicked.connect(CalTotal)
    menu.reset.clicked.connect(resetAll)
    menu.quit.clicked.connect(quitall)
    menu.payment.clicked.connect(choosePayment)
    ch_pay.qrcode.clicked.connect(qrcode_payment)
    qr.paymentDone.clicked.connect(Payment_done)
    ch_pay.cash.clicked.connect(cash_payment)

    sys.exit(app.exec_())
