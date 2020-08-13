from flask import Flask, render_template, request, flash,session
import mysql.connector
from werkzeug.utils import redirect
import os

app = Flask(__name__)
app.secret_key=os.urandom(24)

conn = mysql.connector.connect(
    host="localhost",  # hostname
    user="root",  # the user who has privilege to the db
    passwd="ashish",  # password for user
    database="login_db",  # database name
    auth_plugin='mysql_native_password',
)
cursor = conn.cursor()


@app.route('/index')
def index():
    if 'id' in session:
        return render_template('index.html')
    else:
        return redirect('/')


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/login_validation', methods=['POST'])
def login_validation():
    email = request.form.get('email')
    password = request.form.get('password')
    cursor.execute("select * from users where email like '{}' and password like '{}'".format(email, password))
    user = cursor.fetchall()
    if len(user) > 0:
        session['id']=user[0][0]
        return redirect('index')
    else:
        return redirect('login')


@app.route('/add_data', methods=['POST'])
def add_data():
    username = request.form.get('username')
    email = request.form.get('uemail')
    password = request.form.get('upassword')
    cursor.execute(
        """insert into users (id,username,email,password) values (NULL,'{}','{}','{}')""".format(username, email, password))
    conn.commit()
    cursor.execute("select * from users where email like '{}' and password like '{}'".format(email, password))
    user = cursor.fetchall()
    session['id'] = user[0][0]
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
