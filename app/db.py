import sqlite3

DB_FILE = "data.db"

db = None

def db_connect():
    global db
    db = sqlite3.connect(DB_FILE)
    return db.cursor()

def db_close():
    db.commit()
    db.close()

def db_table_inits():
    c = db_connect()
    c.execute("CREATE TABLE IF NOT EXISTS users (username text, password text)")
    db_close()

def check_if_username_avaliable(username):
    c = db_connect()
    c.execute('SELECT username FROM users WHERE username=?',(username,))
    username_status = c.fetchone()
    db_close()
    return username_status == None

def add_user(username, password):
    if check_if_username_avaliable(username):
        c = db_connect()
        c.execute('INSERT INTO users VALUES (?,?)',(username,password))
        db_close()
        return True
    return False

def check_credentials(username, password):
    c = db_connect()
    c.execute('SELECT * FROM users WHERE username=? AND password=?',(username,password))
    username_status = c.fetchone()
    db_close()
    # print(username_status)
    return username_status != None


if __name__ == '__main__':
    db_table_inits()