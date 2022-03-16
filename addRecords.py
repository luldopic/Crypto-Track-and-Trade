import mysql.connector.errors

import livecoinapi
import CryptoSQL
import json
import requests
from datetime import datetime

headers = {
            'content-type': 'application/json',
            'x-api-key': 'e5d88ba2-cbea-43e5-8dd8-9b9e7d0bdc05'
}

class updateDatabase:
    def __init__(self):
        self.DB = CryptoSQL.CryptoDB()
        self.coin_list = self.get_coin_list()

    def convertUNIXToDateTime(self, unix):
        converted = datetime.fromtimestamp(int(unix)).strftime('%Y-%m-%d %H:%M:%S')
        return converted


    def get_coin_list(self):
        url = "https://api.livecoinwatch.com/coins/list"

        payload = json.dumps({
            "currency": "USD",
            "sort": "rank",
            "order": "ascending",
            "offset": 0,
            "limit": 100,
            "meta": False
        })
        response = requests.request("POST", url, headers=headers, data=payload)
        return json.loads(response.text)

    def updateEntryCount(self):
        rank = 1
        for coin in self.coin_list:
            self.DB.addCoin(coin.get("code"), rank)
            rank = rank+1
            self.DB.UpdateEntryCount(coin.get("code"))

    def addYearRecord(self,year):
        month_list = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        API = livecoinapi.coin_data()
        for coin in self.coin_list:
            for month in range(12):
                BTC2021 = API.get_month_historical(coin["code"], year, month+1)
                BTC2021 = BTC2021["history"]
                for entry in BTC2021:
                    try:
                        self.DB.addRecord(coin["code"], entry)
                        print("Entry added for ", coin["code"], " for ", month_list[month])
                    except mysql.connector.errors.IntegrityError:
                        print("Double entry")
                    except mysql.connector.errors.ProgrammingError as e:
                        print("coin ", coin["code"], "caused error", e)

print("wait")
