# -*- coding: utf-8 -*-
"""
Retrieve data from LiveCoinWatch
"""

import requests
import json
from datetime import datetime, timedelta
import time


class coin_data:
    def __init__(self):
        self.headers = {
            'content-type': 'application/json',
            'x-api-key': 'e5d88ba2-cbea-43e5-8dd8-9b9e7d0bdc05'
        }

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
            "limit": 100,
            "meta": False
        })
        response = requests.request("POST", url, headers=self.headers, data=payload)
        return json.loads(response.text)

    def convertUNIX(self, date):
        date = int(time.mktime(date.timetuple())) * 1000
        return date
