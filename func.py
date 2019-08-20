from database.database import Database
import re

def chat_id_found(chat_id):
    db = Database()
    db.query("SELECT chat_id FROM profile WHERE chat_id = %s;", (chat_id, ))
    items = [item for item in db.data()]
    db.close()
    return True if len(items) > 0 else False

def chat_id_add(chat_id):
    db = Database()
    db.query("INSERT INTO profile (chat_id) VALUES (%s);", (chat_id, ))
    db.close()

def chat_id_del(chat_id):
    db = Database()
    db.query("DELETE FROM profile WHERE chat_id = %s;", (chat_id, ))
    db.close()

def column_add(chat_id, column, column_value):
    db = Database()
    db.query("UPDATE profile SET " + column + " = %(column_value)s WHERE chat_id = %(chat_id)s;", ({'column_value': column_value, 'chat_id': chat_id}))
    db.close()

def column_take(chat_id, column):
    db = Database()
    db.query("SELECT " + column + " FROM profile WHERE chat_id = %s;", (chat_id, ))
    items = [item for item in db.data()]
    db.close()
    return items[0][0]

def check_full_name(text):
    result = re.findall(r'^[^a-z|A-Z|а-я|А-Я|0-9]*([a-z|A-Z|а-я|А-Я]+[\s]+[a-z|A-Z|а-я|А-Я]+)[^a-z|A-Z|а-я|А-Я|0-9]*$', text)
    if len(result) > 0:
        first, last = result[0].split()
        first = first.lower(); first = first[0].upper() + first[1:]
        last = last.lower(); last = last[0].upper() + last[1:] # способ лучше????
        if len(first) > 16: first = first[:16] + "."
        if len(last) > 16: last = last[:16] + "."
        return first, last
    else:
        return None

if __name__ == '__main__':
    # full_name = check_full_name("Petryhaaaaaaaaaaa botin")
    # print(full_name, type(full_name))
    # first, last = full_name
    # print(first, last, type(first), type(last))

    chat_id_del(446162145)
    chat_id_del(385778185)
    chat_id_del(192507315)
    chat_id_del(349441425)
    chat_id_del(932510019)
    # print(chat_id_found(1231))
    # print(chat_id_add(1231))
    # print(chat_id_found(1231))
    # print(chat_id_del(1231))
    # print(chat_id_found(1231))
