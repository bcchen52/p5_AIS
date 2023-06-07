from flask import Flask,render_template,session,request,redirect
from functools import wraps
from db import *
from secrets import token_bytes

app = Flask(__name__)
app.secret_key = token_bytes(32)
# app.secret_key = 'foo'


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        username = session.get("username")
        if username is None:
            return redirect("/")
        return f(*args, **kwargs)
    return decorated_function

@app.route('/', methods=['GET','POST'])
# @login_required
def home():
    username = session.get('username')
    if session.get('username') is None:
        return render_template('landing.html')
    # tags = [(0,'red','school'),(1,'purple','purple'),(2,'','home'),(3,'orange','orange')]
    tags = get_all_tags(username)
    return render_template('home.html',username=username,tags=tags)

@app.route('/create-new-task', methods=['GET','POST'])
# @login_required
def add_task():
    # if request.method == 'POST':
    #     print(f'{request.form = }')
    return render_template('create-task.html',username=session.get('username'))

@app.route('/tasks/<task_id>/edit', methods=['GET','POST'])
@login_required
def edit_task(task_id):
    # if request.method == 'POST':
    #     print(f'{request.form = }')
    return render_template('edit-task.html',task_id=task_id,username=session.get('username'))

@app.route('/tasks/<task_id>', methods=['GET','POST'])
@login_required
def view_task(task_id):
    title = 'test task'
    # description = 'this is a test task\nafter a newline'
    description = ['this is a test task','after a newline']
    return render_template('view-task.html',title=title,description=description,username=session.get('username'))

@app.route('/create-new-tag', methods=['GET','POST'])
# @login_required
def add_tag():
    username=session.get('username')
    if request.method == 'POST':
        tag_name = request.form['tag-name']
        color = request.form['color']
        create_tag(username,color,tag_name)
        return redirect('/')
    return render_template('create-tag.html',username=username)


@app.route('/tags', methods=['GET'])
# @login_required
def tag_list():
    username=session.get('username')
    # tags = [(0,'red','school'),(1,'purple','purple'),(2,'','home'),(3,'orange','orange')]
    tags = get_all_tags(username)
    return render_template('tags.html',tags=tags,username=username)

@app.route('/tags/<tag_id>/edit', methods=['GET','POST'])
# @login_required
def edit_tag(tag_id):
    username=session.get('username')
    if request.method == 'POST':
        tag_name = request.form['tag-name']
        color = request.form['color']
        update_tag(color,tag_name,tag_id)
        return redirect('/')
    tag_info = get_tag_info(tag_id)
    # tag_info = (tag_id,'purple','some-tag')
    return render_template('edit-tag.html',tag_info=tag_info,username=username)


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # print(request.form)
        db_table_inits()
        correct_credentials = check_credentials(username, password)
        if correct_credentials:
            session['username'] = username
            return redirect('/')
        else:
            return render_template('login.html', error = True)
    return render_template('login.html')

@app.route('/signup', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirmation = request.form['confirmation']
        # print(request.form)
        if password != confirmation:
            return render_template('signup.html', confirmation=True)
        db_table_inits()
        added_user = add_user(username, password)
        if added_user:
            session['username'] = username
            return redirect('/login')
        else:
            return render_template('signup.html', error = True)
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('username')
    return render_template('landing.html')

if __name__ == '__main__':
    app.debug = True
    app.run()