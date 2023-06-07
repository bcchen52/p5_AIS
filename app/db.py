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
    c.execute("CREATE TABLE IF NOT EXISTS tags (user_id integer, color text, name text)")
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

# def db_tags_inits():
#     c = db_connect()
#     c.execute("CREATE TABLE IF NOT EXISTS tags (user_id integer, name text, color text)")
#     db_close()

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


def get_user_id(username):
    c = db_connect()
    c.execute('SELECT rowid FROM users WHERE username=?',(username,))
    user_id = int(c.fetchone()[0])
    # print(user_id)
    return user_id



##################### TAGS ########################

def check_tag(username, tag_name):
    c = db_connect()
    user_id = get_user_id(username)
    c.execute('SELECT name FROM tags WHERE user_id=?',(user_id,))
    tag_status = c.fetchone()
    db_close()
    return tag_status == None

def create_tag(username,color,name):
    user_id = get_user_id(username)
    c = db_connect()
    c.execute('INSERT INTO tags VALUES (?,?,?)', (user_id,color,name))
    db_close()

def update_tag(color,name,tag_id):
    # user_id = get_user_id(username)
    c = db_connect()
    c.execute('UPDATE tags SET color=?,name=? WHERE rowid=?', (color,name,tag_id))
    db_close()

def get_all_tags(username):
    '''gets tag_id, color, name for '''
    c = db_connect()
    c.execute('SELECT rowid,color,name FROM tags WHERE user_id=?',(get_user_id(username),))
    # tags = c.fetchone()
    tags = c.fetchall()
    db_close()
    # print(tags)
    return tags

def get_tag_info(tag_id):
    c = db_connect()
    c.execute('SELECT * FROM tags WHERE rowid=?',(tag_id,))
    tag_info = c.fetchone()
    db_close()
    return tag_info
    


if __name__ == '__main__':
    db_table_inits()
    # create_tag('a','purple','added-from-func2')
    # print(get_all_tags('a'))
    # print(get_tag_info(3))
    # print(get_tag_info(4))

    # update_tag('green','green-tag',5)
