import mysql.connector


class CryptoDB:
    def __init__(self):
        self.db = self.connectToDB

    def connectToDB(self):
        with open("MySQLcredentials.json") as handler:
            try:
                credentials = json.load(handler)
                if db_exist:
                    self.db = mysql.connector.connect(host=credentials["host"], user=credentials["user"],
                                                      password=credentials["password"], database="GmailMail")
                else:
                    self.db = mysql.connector.connect(host=credentials["host"], user=credentials["user"],
                                                      password=credentials["password"])
                print("Successful Connection")
            except Exception as e:
                error = str(e)
                if error.__contains__("Unknown database"):
                    raise UnknownDatabase("Database cannot be found")
                else:
                    print(e)
            finally:
                del credentials