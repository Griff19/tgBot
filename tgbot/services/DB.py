import sqlite3


class DB:
    connection = None
    cursor = None

    def __init__(self):
        self.connection = sqlite3.connect("base.db")
        self.cursor = self.connection.cursor()

    def test(self):
        if self.connection:
            print("База подключена!")
        else:
            print("База не подключена")

