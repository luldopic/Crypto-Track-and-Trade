import numpy

import CryptoSQL
import addRecords
import time
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt

class retrieveRecords:
    def __init__(self):
        self.DB = CryptoSQL.CryptoDB()
        record = addRecords.updateDatabase()
        self.coin_list = record.coin_list

    def retrieveRecordByUnix(self, coin, date):
        unixdate = self.UnixDateConversion(date)
        SQL = "SELECT * FROM {coin} WHERE unixdate = {unixdate}".format(coin=coin, unixdate=unixdate)
        res = self.DB.executeSQLCursor(SQL)
        record = res[0]
        return record

    def retrieveAllRecord(self, coin):
        SQL = "SELECT * FROM {coin}".format(coin=coin)
        res = self.DB.executeSQLCursor(SQL)
        return self.resultArray(res)

    def retrieveMonth(self,coin, dateFrom,deltaMonth=1):
        dateTo = dateFrom-timedelta(days=30*deltaMonth)
        unixdateFrom = self.UnixDateConversion(dateFrom)
        unixdateTo = self.UnixDateConversion(dateTo)
        SQL = "SELECT * FROM {coin} WHERE unixdate BETWEEN {v1} AND {v2}".format(coin=coin,
                                                                                    v1=unixdateFrom,
                                                                                    v2=unixdateTo)
        res = self.DB.executeSQLCursor(SQL)
        return self.resultArray(res)

    def retrieveWeek(self,coin, dateFrom,deltaWeek=1):
        dateTo = dateFrom-timedelta(weeks=deltaWeek)
        unixdateFrom = self.UnixDateConversion(dateFrom)
        unixdateTo = self.UnixDateConversion(dateTo)
        SQL = "SELECT * FROM {coin} WHERE unixdate BETWEEN {v1} AND {v2}".format(coin=coin,
                                                                                    v1=unixdateTo,
                                                                                    v2=unixdateFrom)
        res = self.DB.executeSQLCursor(SQL)
        return self.resultArray(res)

    def UnixDateConversion(self,date):
        return int(time.mktime(date.timetuple())) * 1000

    def resultArray(self,res):
        arr = np.array(res)
        arr = np.transpose(arr)
        return arr

class TechnicalIndicators:
    def __init__(self, prediction_date, coin_name):
        self.date = prediction_date
        self.coin = coin_name
        self.recordFunc = retrieveRecords()
        self.calculateIndicators()

    def calculateIndicators(self):
        self.RSI()

    def RSI(self):
        records = self.recordFunc.retrieveWeek(self.coin,self.date,2)
        date_list = records[0]
        timestuff = []
        for date_i in range(len(date_list)-1):
            timeD =  date_list[date_i+1]-date_list[date_i]
            timestuff.append(timeD)


        rate_list = records[1]
        neglist = []
        poslist = []
        for rate_index in range(len(rate_list)-1):
            changes = rate_list[rate_index+1]-rate_list[rate_index]
            if changes > 0:
                poslist.append(changes)
            elif changes < 0:
                neglist.append(changes)
            else:
                pass
        negavg = numpy.mean(neglist)
        posavg = numpy.mean(poslist)
        RSI = 100 - (100/(1+(posavg/negavg)))
        self.RSI = RSI

date =datetime(2021,10,30)
Indicators = TechnicalIndicators(date,"BTC")
RSI = Indicators.RSI

"""
test = Predict1hour()
testdate = datetime(2021, 1, 1, 0, 0, 2)
record = test.retrieveAllRecord("BTC")
arr = np.array(record)
arr = np.transpose(arr)
lab = ["Date","Rate", "Volume", "Cap", "Liquidity"]
x = 1
y = 3
plt.scatter(arr[x],arr[y])
plt.xlabel(lab[x])
plt.ylabel(lab[y])
plt.show()
pass
"""