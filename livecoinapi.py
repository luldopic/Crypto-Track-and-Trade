# -*- coding: utf-8 -*-
"""
Retrieve data from LiveCoinWatch
"""

import requests
import json
from datetime import datetime, timedelta
import time
import CryptoSQL


class coin_data:
    def __init__(self):
        self.headers = {
            'content-type': 'application/json',
            'x-api-key': 'e5d88ba2-cbea-43e5-8dd8-9b9e7d0bdc05'
        }

    def get_month_historical(self, coin, year, month):
        date = datetime(year, month, 1)
        month_length = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        delta = month_length[month-1]
        return self.get_historical_single(coin, date, delta)

    def get_day_historical(self,coin, year, day):
        date = datetime(year-1, 12, 31) + timedelta(days=day)
        DB = CryptoSQL.CryptoDB()
        SQL = "SELECT age FROM coin_list WHERE coin_name='{coin}'".format(coin=coin)
        res = DB.executeSQLCursor(SQL)
        age = res[0][0]
        diff = datetime.now()-date
        diff = diff.days
        if diff<age:
            return self.get_historical_single(coin, date, 1)
        else:
            print("Coin is too young")
            raise CoinTooYoung

    def get_year_historical(self, coin, year):
        date = datetime(year, 1, 1)
        return self.get_historical_single(coin, date, 365)

    def get_historical_single(self, coin, date, delta=1, currency="USD"):
        url = "https://api.livecoinwatch.com/coins/single/history"
        payload = json.dumps(
            {
                "currency": currency,
                "code": coin,
                "start": self.convertUNIX(date),
                "end": self.convertUNIX(date + timedelta(days=delta))
            })

        response = requests.request("POST", url, headers=self.headers, data=payload)

        return json.loads(response.text)

    def get_current_single(self, coin):
        url = "https://api.livecoinwatch.com/coins/single"

        payload = json.dumps({
            "currency": "USD",
            "code": coin,
            "meta": False
        })

        response = requests.request("POST", url, headers=self.headers, data=payload)
        dict = json.loads(response.text)
        dict["date"] = self.convertUNIX(datetime.now())
        return dict

    def get_coin_list(self):
        url = "https://api.livecoinwatch.com/coins/list"

        payload = json.dumps({
            "currency": "USD",
            "sort": "rank",
            "order": "ascending",
            "offset": 0,
            "limit": 200,
            "meta": True
        })
        response = requests.request("POST", url, headers=self.headers, data=payload)
        return json.loads(response.text)

    def convertUNIX(self, date):
        date = int(time.mktime(date.timetuple())) * 1000
        return date


class CoinTooYoung(Exception):
    pass

