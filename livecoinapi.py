# -*- coding: utf-8 -*-
"""
Retrieve data from LiveCoinWatch
"""

import requests
import json
from datetime import datetime, timedelta
import time


class coin_data:
    def __init__(self, coin_list):
        self.code_list = coin_list
        self.headers = {
            'content-type': 'application/json',
            'x-api-key': 'e5d88ba2-cbea-43e5-8dd8-9b9e7d0bdc05'
        }

    def get_historical_single(self, currency, coin, date, delta):
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

    def get_current_single(self,coin):

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

    def convertUNIX(self, date):
        date = int(time.mktime(date.timetuple())) * 1000
        return date
