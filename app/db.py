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
    c.execute("CREATE TABLE IF NOT EXISTS users (user_id integer primary key, username text, password text)")
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

def db_tags_inits():
    c = db_connect()
    c.execute("CREATE TABLE IF NOT EXISTS tags (user_id integer, name text, color text)")
    db_close()

def db_tasks_inits():
    c = db_connect()
    c.execute("CREATE TABLE IF NOT EXISTS tasks (user_id integer, title text, description text, status text, date text, tag_ids text)")
    db_close()

def get_tasks(username):
    c = db_connect()
    user_id = get_user_id(username)
    c.execute("SELECT * from tasks where user_id = ?",(user_id))
    db_close()

def make_task(username, title, description, date, tag_id):
    c = db_connect()
    user_id = get_user_id(username)
    c.execute("insert into tags values (?,?,?,?,?,?)",(user_id, title, description, "incomplete", date, tag_id))
    db_close()

#def edit_task(tag_name,):

'''
def get_tag_id(tag_name):
    c = db_connect()
    c.execute('SELECT rowid FROM tags WHERE name=?',(tag_name))
    user_id = c.fetchone()
    return tag_id
    '''


def get_user_id(username):
    c = db_connect()
    c.execute('SELECT rowid FROM users WHERE username=?',(username,))
    user_id = c.fetchone()
    return user_id


def check_tag(username, tag_name):
    c = db_connect()
    user_id = get_user_id(username)
    c.execute('SELECT name FROM tags WHERE user_id=?',(user_id,))
    tag_status = c.fetchone()
    db_close()
    return tag_status == None

def create_tag(username, tag_name):
    pass
    


if __name__ == '__main__':
    db_table_inits()
    db_tags_inits()
    db_tasks_inits()