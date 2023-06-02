from flask import Flask,render_template,session,request,redirect
from functools import wraps
from db import *
from secrets import token_bytes

app = Flask(__name__)
app.secret_key = token_bytes(32)

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
    if session.get('username') is None:
        return render_template('landing.html')
    return render_template('home.html',username=session.get('username'))

@app.route('/create-new-task', methods=['GET','POST'])
@login_required
def add_task():
    # if request.method == 'POST':
    #     print(f'{request.form = }')
    return render_template('create-task.html')

@app.route('/create-new-tag', methods=['GET','POST'])
# @login_required
def add_tag():
    # if request.method == 'POST':
    #     print(f'{request.form = }')
    return render_template('create-tag.html')

# @app.route('/', methods=['GET'])
# def landing():
#     return render_template('landing.html')


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