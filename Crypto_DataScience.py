import CryptoSQL
import addRecords
import time
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

class Predict1hour:
    def __init__(self):
        self.DB = CryptoSQL.CryptoDB()
        record = addRecords.updateDatabase()
        record.updateEntryCount()
        self.coin_list = record.get_coin_list()

    def retrieveRecordByUnix(self, coin, date):
        unixdate = int(time.mktime(date.timetuple())) * 1000
        SQL = "SELECT * FROM {coin} WHERE unixdate = {unixdate}".format(coin=coin, unixdate=unixdate)
        res = self.DB.executeSQLCursor(SQL)
        record = res[0]
        return record

    def retrieveAllRecord(self, coin):
        SQL = "SELECT * FROM {coin}".format(coin=coin)
        res = self.DB.executeSQLCursor(SQL)
        arr = np.array(res)
        arr = np.transpose(arr)
        return arr

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