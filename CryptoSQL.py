import mysql.connector
import json


class CryptoDB:
    def __init__(self):
        self.connectToDB()

    def addCoin(self, coin_name):
        if not self.coinTableExists(coin_name):
            SQL = "CREATE TABLE {coin_name} " \
                  "(unixdate BIGINT  NOT NULL, " \
                  "rate BIGINT NOT NULL, " \
                  "volume DOUBLE(26,13), " \
                  "cap DOUBLE (26,13), " \
                  "liquidity DOUBLE(26,13)," \
                  "PRIMARY KEY (unixdate))".format(coin_name=coin_name)
            self.executeSQLCursor(SQL)
            SQL = "INSERT INTO coin_list (coin_name) VALUES ('{coin_name}')".format(coin_name=coin_name)
            self.executeSQLCursor(SQL)
        else:
            print("Coin already added")

    def addRecord(self, coin_name, record):
        columns = str(tuple(record.keys())).replace("'", "")
        values = str(tuple(record.values())).replace("\"", "'")
        SQL = "INSERT INTO {table} {columns} VALUES {values}".format(table=coin_name, columns=columns, values=values)
        self.executeSQLCursor(SQL)
        self.db.commit()

    def coinTableExists(self, coin_name):
        SQL = "SHOW TABLES LIKE '{name}'".format(name=coin_name)
        res = self.executeSQLCursor(SQL)
        if len(res) == 0:
            return False
        else:
            return True

    def executeSQLCursor(self, command):
        cursor = self.db.cursor()
        cursor.reset()
        cursor.execute(command)
        res = cursor.fetchall()
        cursor.close()
        return res

    def connectToDB(self):
        with open("MySQLcredentials.json") as handler:
            try:
                credentials = json.load(handler)
                self.db = mysql.connector.connect(host=credentials["host"], user=credentials["user"],
                                                  password=credentials["password"], database="cryptotrack")
                print("Successful Connection")

            except Exception as e:
                print(e)
            finally:
                if 'credentials' in locals():
                    del credentials
                else:
                    pass
