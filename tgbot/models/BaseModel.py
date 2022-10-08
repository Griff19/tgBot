from tgbot.services.DB import DB


class BaseModel:
    table = ''

    def __init__(self):
        self.db = DB()

    def insert(self, values):
        self.db.cursor.execute(f"INSERT OR IGNORE {self.table} VALUES ")