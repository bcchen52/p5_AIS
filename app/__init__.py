from flask import Flask,render_template,session,request,redirect
from functools import wraps

app = Flask(__name__)

# def login_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         username = session.get("username")
#         if username is None:
#             return redirect("/")
#         return f(*args, **kwargs)
#     return decorated_function


@app.route('/', methods=['GET','POST'])
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET','POST'])
def login():
    return render_template('login.html')

@app.route('/signup', methods=['GET','POST'])
def register():
    return render_template('signup.html')

if __name__ == '__main__':
    app.debug = True
    app.run()