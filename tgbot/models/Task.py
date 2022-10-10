from tgbot.models.Account import Account
from tgbot.models.BaseModel import BaseModel
from tgbot.services.DB import DB
import datetime


class Task(BaseModel):

    table = 'task'

    STATUS_WORK = 'work'
    STATUS_CLOSE = 'close'
    STATUS_BACK = 'back'

    # @classmethod
    # def create_task(cls, user_id):
    #     db = DB()
    #     user = User(user_id=user_id)
    #     date = str(datetime.datetime.now())[:10]
    #     db.cursor.execute("INSERT INTO task (user_id, name, description, status) VALUES (?, ?, ?, ?)", (user_id, user_id, date, cls.STATUS_WORK))
    #     task_id = db.cursor.lastrowid
    #     items = user.get_accounts()
    #     for item in items:
    #         db.cursor.execute("UPDATE account SET task_id = ?, status = ? WHERE id = ?;", (task_id, Account.STATUS_TASK, item[0]))
    #
    #     db.connection.commit()






