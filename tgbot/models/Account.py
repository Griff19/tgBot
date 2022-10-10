from tgbot.models.BaseModel import BaseModel
from tgbot.services.DB import DB


class Account(BaseModel):
    table = 'account'

    STATUS_NEW = 'new'
    STATUS_WORK = 'work'
    STATUS_TASK = 'task'
    STATUS_PROCESSED = 'processed'

    @classmethod
    def get_next_block(cls, user_id=None, limit=5, factor=0, old_rows=None):
        offset = limit * factor
        db = DB()
        if not old_rows:
            rows = db.cursor.execute("SELECT * FROM account WHERE status = ? AND user_id = ?;", (cls.STATUS_WORK, user_id)).fetchall()
            if rows:
                return rows

        if old_rows:
            for row in old_rows:
                db.cursor.execute("UPDATE account SET status = ?, user_id = ? WHERE id = ?", (cls.STATUS_NEW, None, row[0]))
            db.connection.commit()
        rows = db.cursor.execute("SELECT * FROM account WHERE status = ? LIMIT ?, ?;", (cls.STATUS_NEW, offset, limit)).fetchall()
        for row in rows:
            db.cursor.execute("UPDATE account SET status = ?, user_id = ? WHERE id = ?", (cls.STATUS_WORK, user_id, row[0]))
        db.connection.commit()
        return rows

