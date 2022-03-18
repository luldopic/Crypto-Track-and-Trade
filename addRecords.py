import mysql.connector.errors
import livecoinapi
import CryptoSQL
from datetime import datetime

headers = {
            'content-type': 'application/json',
            'x-api-key': 'e5d88ba2-cbea-43e5-8dd8-9b9e7d0bdc05'
}

class updateDatabase:
    def __init__(self):
        self.DB = CryptoSQL.CryptoDB()
        self.update_coin_list_from_LiveCoin()
        self.coin_list = self.get_coin_list_from_SQLServer()
        self.updateEntryCount()

    def convertUNIXToDateTime(self, unix):
        converted = datetime.fromtimestamp(int(unix)).strftime('%Y-%m-%d %H:%M:%S')
        return converted

    def get_coin_list_from_SQLServer(self):
        SQL = "SELECT coin_name from coin_list ORDER BY age DESC"
        res = self.DB.executeSQLCursor(SQL)
        coin_list = []
        for coin in res:
            coin_list.append(coin[0])
        return coin_list

    def update_coin_list_from_LiveCoin(self):
        API = livecoinapi.coin_data()
        coin_list = API.get_coin_list()
        try:
            for coin in coin_list:
                SQL = "UPDATE coin_list SET coin_rank={rank}, age = {age} WHERE coin_name = '{name}'".format\
                    (rank=coin["rank"],age=coin["age"], name=coin["code"])
                self.DB.executeSQLCursor(SQL)
        except:
            print("")

    def updateEntryCount(self):
        rank = 1
        for coin in self.coin_list:
            #self.DB.addCoin(coin["code"], rank)
            rank = rank+1
            self.DB.UpdateEntryCount(coin)

    def addYearRecordDay(self, year):
        API = livecoinapi.coin_data()
        for coin in self.coin_list:
            print(coin)
            for day in range(365):
                print(day)
                try:
                    BTC2021 = API.get_day_historical(coin, year, day+1)
                    BTC2021 = BTC2021["history"]
                    for entry in BTC2021:
                        try:
                            self.DB.addRecord(coin, entry)
                            print("Entry added for ", coin, " for ", day)
                        except mysql.connector.errors.IntegrityError:
                            print("Double entry")
                        except mysql.connector.errors.ProgrammingError:
                            print(coin)
                            pass
                except livecoinapi.CoinTooYoung:
                    print("Coin too young")

    def addYearRecordMonth(self,year):
        month_list = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        API = livecoinapi.coin_data()
        for coin in self.coin_list:
            print(coin)
            for month in range(12):
                BTC2021 = API.get_month_historical(coin, year, month+1)
                BTC2021 = BTC2021["history"]
                for entry in BTC2021:
                    try:
                        self.DB.addRecord(coin, entry)
                        print("Entry added for ", coin, " for ", month_list[month])
                    except mysql.connector.errors.IntegrityError:
                        print("Double entry")
                    except mysql.connector.errors.ProgrammingError as e:
                        print("coin ", coin, "caused error", e)

