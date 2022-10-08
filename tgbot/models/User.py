from tgbot.models.BaseModel import BaseModel
from tgbot.services.DB import DB


class User(BaseModel):
    table = 'user'

    STATUS_NEW = 'new'
    STATUS_MEMBER = 'member'
    STATUS_ADMIN = 'admin'
    STATUS_BLOCkED = 'blocked'

    def __init__(self, id_user=0, alias=''):
        super().__init__()
        user = None
        if id_user > 0:
            user = self.find_user_by_id(id_user)
        else:
            print("Пользователь не найден")

        if alias != '':
            user = self.find_user_by_alias(alias)
        else:
            print("Пользователь на найден")

        if user:
            self.user_id = user[0]
            self.alias = user[1]
            self.name = user[2]
            self.surname = user[3]
            self.status = user[4]
            self.note = user[5]

    @classmethod
    def select_all(cls):
        db = DB()
        rows = db.cursor.execute("SELECT * FROM user;").fetchall()
        for row in rows:
            print(row)

    @classmethod
    def select_new(cls):
        db = DB()
        rows = db.cursor.execute("SELECT id, alias, name, surname FROM user WHERE status = 'new';").fetchall()
        return rows

    @classmethod
    def find_user_by_id(cls, id_user):
        db = DB()
        user = db.cursor.execute("SELECT * FROM user WHERE id = ?", (id_user,)).fetchall()
        print(user)
        return user

    @classmethod
    def find_user_by_alias(cls, alias):
        db = DB()
        user = db.cursor.execute("SELECT * FROM user WHERE alias = ?", (alias,)).fetchall()
        return user

    @classmethod
    def insert(cls, id_user=0, alias='', name='', surname='', status='', note=''):
        db = DB()
        db.cursor.execute("INSERT OR IGNORE INTO user VALUES (?, ?, ?, ?, ?, ?);", (id_user, alias, name, surname, status, note))
        db.connection.commit()

    @classmethod
    def update(cls, user_id=None, status=''):
        db = DB()
        db.cursor.execute("UPDATE user SET status = ? WHERE id = ?", (status, user_id))
        db.connection.commit()
