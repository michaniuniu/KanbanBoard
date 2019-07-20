from flask import Flask, render_template, json, request, session, redirect, url_for, send_from_directory
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json

with open("config.json") as outfile:
    config = json.load(outfile)
    for record in config['KANBAN']:
        SECRET_KEY = record['SECRET_KEY']
        MYSQL_DATABASE_USER = record['MYSQL_DATABASE_USER']
        MYSQL_DATABASE_PASSWORD = record['MYSQL_DATABASE_PASSWORD']
        MYSQL_DATABASE_DB = record['MYSQL_DATABASE_DB']
        MYSQL_DATABASE_HOST = record['MYSQL_DATABASE_HOST']

mysql = MySQL()
app = Flask(__name__)

app.secret_key = SECRET_KEY
app.config['MYSQL_DATABASE_USER'] = MYSQL_DATABASE_USER
app.config['MYSQL_DATABASE_PASSWORD'] = MYSQL_DATABASE_PASSWORD
app.config['MYSQL_DATABASE_DB'] = MYSQL_DATABASE_DB
app.config['MYSQL_DATABASE_HOST'] = MYSQL_DATABASE_HOST
mysql.init_app(app)


@app.route("/")
def main():
    return render_template("index.html")


@app.route('/showSignUp')
def show_sign_up():
    return render_template('signup.html')


@app.route('/signUp', methods=['POST'])
def sign_up():
    try:
        _name = request.form['login']
        _email = request.form['email']
        _password = request.form['password']

        if _name and _email and _password:

            conn = mysql.connect()
            cursor = conn.cursor()
            _hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_createUser', (_name, _email, _hashed_password))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message': 'User created successfully !'})
            else:
                return json.dumps({'error': str(data[0])})
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error': str(e)})
    finally:
        cursor.close()
        conn.close()


@app.route('/showSignIn')
def show_sign_in():
    return render_template('signin.html')


@app.route('/validateLogin', methods=['POST'])
def validate_login():
    try:
        _username = request.form['login']
        _password = request.form['password']

        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_validateLogin', (_username,))
        data = cursor.fetchall()

        if len(data) > 0:
            if check_password_hash(str(data[0][3]), _password):
                session['user'] = data[0][0]
                return redirect(url_for('userHome'))
            else:
                return render_template('error.html', error='Wrong Email address or Password.')
        else:
            return render_template('error.html', error='Wrong Email address or Password.')

    except Exception as e:
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        con.close()


@app.route('/userHome')
def user_home():
    if session.get('user'):
        return render_template('userHome.html')
    else:
        return render_template('error.html', error='Unauthorized Access')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


if __name__ == "__main__":
    app.run()
