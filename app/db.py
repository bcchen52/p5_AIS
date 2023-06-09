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
    c.execute("CREATE TABLE IF NOT EXISTS tags (user_id integer, color text, name text)")
    c.execute("CREATE TABLE IF NOT EXISTS tasks (user_id int, title text, \
              description text, status int, year int, month int, day int, \
              hour int, min int, tags text)")
    db_close()

def get_user_id(username):
    c = db_connect()
    c.execute('SELECT rowid FROM users WHERE username=?',(username,))
    user_id = int(c.fetchone()[0])
    # print(user_id)
    return user_id

################ LOGGING IN/REGISTERING ###############

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


################### TASKS #####################
'''
user_id, title, description, status, 
year, month, day, hour, min, tags
'''

def get_tasks(username):
    c = db_connect()
    user_id = get_user_id(username)
    c.execute("SELECT * from tasks where user_id = ?",(user_id))
    db_close()

# format: YYYY-MM-DDThh:mm
def get_timestamp_tuple(timestamp_str):
    year = int(timestamp_str[:4])
    month = int(timestamp_str[5:7])
    day = int(timestamp_str[8:10])
    hour = int(timestamp_str[11:13])
    minute = int(timestamp_str[14:16])
    return (year,month,day,hour,minute)

def create_new_task(username, title, timestamp_str, status, tags, description):
    user_id = get_user_id(username)
    # print(f'{date = }')
    # print(f'{tags = }')
    timestamp = get_timestamp_tuple(timestamp_str)
    c = db_connect()
    c.execute('INSERT INTO tasks VALUES (?,?,?,?,?,?,?,?,?,?)', \
              (user_id, title, description, status, *timestamp, tags))
    db_close()

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

    print(get_timestamp_tuple('2017-06-01T08:30'))
    print(get_timestamp_tuple('2023-06-09T01:14'))

    # username = 'a'
    # user_id = get_user_id(username)
    # title = 'title in db'
    # description = 'desc in db'
    # status = 1
    # timestamp = (2023,6,14,15,8)
    # tags = '12380,19203'

    # timestamp_str = '2023-06-09T01:14'

    # create_new_task(username, title, timestamp_str, status, tags, description)

    # c = db_connect()
    # c.execute('INSERT INTO tasks VALUES (?,?,?,?,?,?,?,?,?,?)', \
    #           (user_id, title, description, status, *timestamp, tags))
    # db_close()
