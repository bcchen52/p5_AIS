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

STATUS_NAMES = ['not started','in progress','completed']
STATUS_CLASSES = ['not-started','in-progress','completed']

def get_task_info(row):
    task_dict = dict()
    task_dict['task_id'] = row[0]
    task_dict['title'] = row[2]
    # task_dict['description'] = row[3].replace('\n', '<br>')
    task_dict['description'] = row[3]
    task_dict['status-name'] = STATUS_NAMES[row[4]]
    task_dict['status-class'] = STATUS_CLASSES[row[4]]
    task_dict['status'] = row[4]
    task_dict['due-date'] = f'{row[5]:04d}-{row[6]:02d}-{row[7]:02d} {row[8]:02d}:{row[9]:02d}'
    task_dict['tags'] = get_tags_from_csv(row[10])
    # task_dict['tag_ids'] = tuple(map(int,row[10].split(',')))
    return task_dict

def get_task_info_from_id(task_id):
    c = db_connect()
    c.execute("SELECT rowid,* from tasks where rowid=?",(task_id,))
    row = c.fetchone()
    db_close()
    # print(row)
    return get_task_info(row)

def get_all_tasks(username):
    c = db_connect()
    user_id = get_user_id(username)
    c.execute("SELECT rowid,* from tasks where user_id=? ORDER BY year,month,day,hour,min",(user_id,))
    raw_tasks = c.fetchall()
    db_close()
    tasks = []
    for row in raw_tasks:
        task_dict = get_task_info(row)
        tasks.append(task_dict)
    return tasks

def get_all_tasks_by_tags(username,tags):
    all_tasks = get_all_tasks(username)
    print(f'{all_tasks = }')
    print(f'{tags = }')
    tasks = []
    for task in all_tasks:
        print(task['tags'])
        for tag in task['tags']:
            # print(tag)
            tag_id = tag[0]
            print(f'{tag_id = }')
            if tag_id in tags:
                tasks.append(task)
                break
    return tasks

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

def change_task(task_id, title, timestamp_str, status, tags, description):
    # user_id = get_user_id(username)
    timestamp = get_timestamp_tuple(timestamp_str)
    c = db_connect()
    # c.execute('REPLACE INTO tasks VALUES (?,?,?,?,?,?,?,?,?,?)', \
    #         (user_id, title, description, status, *timestamp, tags))
    c.execute('UPDATE tasks SET title=?, \
              description=?, status=?, year=?, month=?, day=?, \
              hour=?, min=?, tags=? WHERE rowid=?', \
              (title, description, status, *timestamp, tags,task_id))
    db_close()

def delete_task(task_id):
    c = db_connect()
    c.execute('DELETE FROM tasks WHERE rowid=?',(task_id,))
    db_close()

def exist_task(task_title):
    c = db_connect()
    c.execute('SELECT title FROM tasks WHERE title=?',(task_title,))
    ans = c.fetchall()
    db_close()
    try:
        a = ans[0]
        return True
    except: 
        return False

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

def get_tags_from_csv(tags_csv):
    if tags_csv == '':
        return []
    tags = []
    str_tag_ids = tags_csv.split(',')
    # print(str_tag_ids)
    for str_tag_id in str_tag_ids:
        tags.append(get_tag_info(int(str_tag_id)))
    return tags

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
    c.execute('SELECT rowid,color,name FROM tags WHERE rowid=?',(tag_id,))
    tag_info = c.fetchone()
    db_close()
    return tag_info

def get_tasks_with_tag(tag_id):
    c = db_connect()
    raw_tasks = []
    for a in tag_id:
        c.execute('SELECT rowid,* FROM tasks WHERE tags LIKE ?;',('%'+a+'%',))
        b = c.fetchall()
        raw_tasks += b
    db_close()

    tasks = []
    for row in raw_tasks:
        task_dict = get_task_info(row)
        tasks.append(task_dict)
    return tasks

# print(get_tasks_with_tag("[1,2]"))
# print()
# print(get_all_tasks('a'))

# if __name__ == '__main__':
#     db_table_inits()
#     # print(get_all_tasks_by_tags('a',(1,)))
#     print(get_task_info_from_id(6))
