from tgbot.models.Account import Account
from tgbot.models.BaseModel import BaseModel
from tgbot.models.Task import Task
from tgbot.services.DB import DB
from tgbot.config import load_config

import datetime


class User(BaseModel):
    table = 'user'

    id = 0
    alias = ''
    name = ''
    surname = ''
    status = ''
    note = ''

    STATUS_NEW = 'new'
    STATUS_MEMBER = 'member'
    STATUS_ADMIN = 'admin'
    STATUS_BLOCkED = 'blocked'

    def __init__(self, user_id=0, alias=''):
        super().__init__()
        user = None
        if user_id > 0:
            user = self.find_user_by_id(user_id)
        else:
            if alias != '':
                user = self.find_user_by_alias(alias)

        if user:
            self.id = user[0]
            self.alias = user[1]
            self.name = user[2]
            self.surname = user[3]
            self.status = user[4]
            self.note = user[5]

    def is_member(self):
        status = self.db.cursor.execute("SELECT status FROM user WHERE id = ?;", (self.id,)).fetchone()
        return status[0] == User.STATUS_MEMBER

    def is_admin(self):
        config = load_config("../../.env")
        return self.id in config.tg_bot.admin_ids

    def get_accounts(self):
        rows = self.db.cursor.execute("SELECT * FROM account WHERE status = ? AND user_id = ?;", (Account.STATUS_WORK, self.id)).fetchall()
        return rows

    def create_task(self):
        date = str(datetime.datetime.now())[:10]
        self.db.cursor.execute("INSERT INTO task (user_id, name, description, status) VALUES (?, ?, ?, ?)",
                          (self.id, self.id, date, Task.STATUS_WORK))
        task_id = self.db.cursor.lastrowid
        items = self.get_accounts()
        for item in items:
            self.db.cursor.execute("UPDATE account SET task_id = ?, status = ? WHERE id = ?;",
                              (task_id, Account.STATUS_TASK, item[0]))

        self.db.connection.commit()

    def get_task(self):
        query = '''SELECT task_id, name, description, alias, a.id FROM task
                   LEFT JOIN account a ON task.id = a.task_id
                   WHERE task.user_id = ? AND task.status = ?'''

        rows = self.db.cursor.execute(query, (self.id, Task.STATUS_WORK)).fetchall()
        return rows

    def close_task(self):
        items = self.get_task()
        if items:
            task_id = items[0][0]
            self.db.cursor.execute("UPDATE task SET status = ? WHERE id = ?;", (Task.STATUS_CLOSE, task_id))
            for item in items:
                self.db.cursor.execute("UPDATE account SET status = ? WHERE id = ?", (Account.STATUS_PROCESSED, item[4]))

            self.db.connection.commit()

    def back_task(self):
        items = self.get_task()
        if items:
            task_id = items[0][0]
            self.db.cursor.execute("UPDATE task SET status = ? WHERE id = ?;", (Task.STATUS_BACK, task_id))
            for item in items:
                self.db.cursor.execute("UPDATE account SET task_id = null, user_id = null, status = ? WHERE id = ?;", (Account.STATUS_NEW, item[4]))

            self.db.connection.commit()

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
    def count_new(cls):
        db = DB()
        count = db.cursor.execute("SELECT count(id) FROM user WHERE status = 'new';").fetchone()
        return int(count[0])

    @classmethod
    def find_user_by_id(cls, user_id):
        db = DB()
        user = db.cursor.execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()

        return user

    @classmethod
    def find_user_by_alias(cls, alias):
        db = DB()
        user = db.cursor.execute("SELECT * FROM user WHERE alias = ?", (alias,)).fetchone()
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
