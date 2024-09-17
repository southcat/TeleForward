import sqlite3

db_path = '/app/messages.db'


def init_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY,
        message_id INTEGER,
        chat_id INTEGER,
        forwarded BOOLEAN
    )
    ''')
    conn.commit()
    conn.close()


def save_message(message_id, chat_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO messages (message_id, chat_id, forwarded) VALUES (?, ?, ?)',
                   (message_id, chat_id, False))
    conn.commit()
    conn.close()


def get_unforwarded_messages():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT message_id, chat_id FROM messages WHERE forwarded = ?', (False,))
    messages = cursor.fetchall()
    conn.close()
    return messages


def get_unforwarded_messages_for_lasts():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT message_id, chat_id FROM messages WHERE forwarded = ? AND exception is null ORDER by '
                   'message_id limit 100', (False,))
    messages = cursor.fetchall()
    conn.close()
    return messages


def mark_as_forwarded(message_id, chat_id, target_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('UPDATE messages SET forwarded = ? WHERE message_id = ? AND chat_id = ? AND target_id= ?',
                   (True, message_id, chat_id, target_id))
    conn.commit()
    conn.close()


def exception_as_forwarded(message_id, chat_id, target_id, exception):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE messages SET forwarded = ? , exception = ? WHERE message_id = ? AND chat_id = ? AND target_id= ?',
        (False, exception, message_id, chat_id, target_id))
    conn.commit()
    conn.close()


def get_all_fordward_chat():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM config WHERE setting_name = ?', ("fordward_chat_list"))
    messages = cursor.fetchall()
    conn.close()
    return messages


def save_accounts(phone_number, session_string):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO accounts (phone_number, session_string) VALUES (?, ?)',
                   (phone_number, session_string))
    conn.commit()
    conn.close()


def update_accounts(phone_number, session_string):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('UPDATE accounts SET session_string = ? WHERE phone_number = ?',
                   (session_string, phone_number))
    conn.commit()
    conn.close()


def get_all_accounts():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT id,phone_number,session_string FROM accounts')
    messages = cursor.fetchall()
    conn.close()
    return messages


def get_all_group(account_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT id,type,account_id,group_name,group_id FROM groups WHERE account_id = ?', (account_id,))
    messages = cursor.fetchall()
    conn.close()
    return messages


def insert_group(account_id, group_id, group_type, grou_name):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO groups (account_id, group_id, type, group_name) VALUES (?, ?, ?, ?)',
                   (account_id, group_id, group_type, grou_name))
    conn.commit()
    conn.close()


def delete_all_group(account_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM groups WHERE account_id = ?', (account_id,))
    conn.commit()
    conn.close()


def get_accounts_by_phone_number(phone_number):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM accounts WHERE phone_number = ? ', (phone_number,))
    messages = cursor.fetchall()
    conn.close()
    return messages


def get_accounts_task_by_id(account_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT id,account_id,chat_id,target_id FROM replay_task WHERE account_id = ? ', (account_id,))
    messages = cursor.fetchall()
    conn.close()
    return messages


def insert_task(accountId, chatId, targetId):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO replay_task (account_id, chat_id, target_id) VALUES (?, ?, ?)',
                   (accountId, chatId, targetId))
    conn.commit()
    conn.close()


def delete_task_by_id(id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM replay_task WHERE id = ?', (id,))
    conn.commit()
    conn.close()


def get_task_by_id(task_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT id,account_id,chat_id,target_id FROM replay_task WHERE id = ?', (task_id,))
    messages = cursor.fetchall()
    conn.close()
    return messages


def get_account_phone_number_by_id(account_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT phone_number FROM accounts WHERE id = ?', (account_id,))
    messages = cursor.fetchall()
    conn.close()
    return messages


# 通用查询方法 直接接收sql
def query(sql):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(sql)
    messages = cursor.fetchall()
    conn.close()
    return messages


# 通用更新方法直接接收sql
def update(sql):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()


# 通用删除方法直接接收sql
def delete(sql):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()


# 通用插入方法直接
def insert(sql):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()
