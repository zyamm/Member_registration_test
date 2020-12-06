import db_access
import config

from flask import Flask, render_template, request, session, redirect
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from datetime import datetime

app = Flask(__name__)


# My page after registration
@app.route('/')
def index():
    if 'user_id' in session and session['user_id']:

        return render_template('index.html')
    return redirect('/login')


# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    # If input is True, return to index ()
    if request.method == 'POST':
        if db_access._is_account_valid(request.form['email'], request.form['password']):
            conn = db_access.conn_f()
            cursor = conn.cursor()
            mysql_cmd = 'select user_id from users where email= "{0}";'.format(
                request.form['email'])
            cursor.execute(mysql_cmd)
            user_id = cursor.fetchone()
            session['user_id'] = user_id[0]

            cursor.close()
            conn.close()

            return redirect('/')  # Move to my page, index()
        # If False, display the login page again
        else:
            e_mess = 'Input is not corrct'
            return render_template('login.html', message=e_mess)
    # Processing when the page is opened for the first time
    return render_template('login.html')


# Member registration page
@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        input_pass = request.form['password']

        hash_pass = generate_password_hash(input_pass)
        date = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

        # Add data to database
        conn = db_access.conn_f()
        cursor = conn.cursor()
        mysql_cmd = 'insert into users(username, email, password, date_time) values("{0}", "{1}", "{2}", "{3}");'.format(username,
                                                                                                                         email,
                                                                                                                         hash_pass,
                                                                                                                         date)
        cursor.execute(mysql_cmd)
        conn.commit()

        cursor.close()
        conn.close()

        # session hold
        session['user_id'] = cursor.lastrowid
        return redirect('/')
    return render_template('sign_up.html')


# Logout page
@app.route('/logout', methods=['GET'])
def logout():
    session.pop('user_id', None)
    return redirect('/login')


# Session encryption
app.secret_key = config.sk

if __name__ == "__main__":
    app.run(port=8000, debug=True)
