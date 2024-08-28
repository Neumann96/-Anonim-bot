import sqlite3


def add(id, name):
    connect = sqlite3.connect('anonim_bot.db')
    cursor = connect.cursor()

    exists = cursor.execute("SELECT 1 FROM users WHERE id = ?", (id,)).fetchone()

    if exists:
        pass
    else:
        try:
            item = []
            item.append(id)
            item.append(name)
            cursor.execute('INSERT INTO users(id, name) VALUES(?, ?);', item)

            connect.commit()
            cursor.close()
            return True
        except:
            pass


def add_message(id, name, ref_id, text):
    connect = sqlite3.connect('anonim_bot.db')
    cursor = connect.cursor()
    try:
        item = []
        item.append(id)
        item.append(name)
        item.append(ref_id)
        item.append(text)

        cursor.execute('INSERT INTO users_message(id, name, id_who, message) VALUES(?, ?, ?, ?);', item)

        connect.commit()
        cursor.close()
    except:
        pass