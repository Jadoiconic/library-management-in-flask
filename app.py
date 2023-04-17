from flask import Flask, render_template, request, session, redirect
import mysql.connector
from datetime import timedelta

app = Flask(__name__)


#! Configure MySQL connection
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="library"
)

app.config['SECRET_KEY'] = 'your_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=7)

mycursor = mydb.cursor()

@app.route('/')
def index():
    return render_template('index.htm')

@app.route('/login')
def loginForm():
    return render_template('login.htm')

@app.route('/signin', methods=['POST'])
def login_post():
    # Get form data
    username = request.form['username']
    password = request.form['password']

    #? Query the users table for the given username and password
    mycursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    users = mycursor.fetchall()

    # Check if the user exists
    if users:
        #? Store the user ID in a session variable
        session['user_id'] = list(users)
        return redirect('/dashboard')
    else:
        return render_template('login.htm', error='Invalid username or password')
    
    
@app.route('/about')
def aboutView():
    return render_template('about.htm')

@app.route('/books')
def serviceView():
    return render_template('service.htm')

@app.route('/dashboard')
def dashboard():
    if len(session) == 0: return render_template('login.htm',error='You must login First')
    user = session['user_id']
    return render_template('Admin/index.htm',user = user)

@app.route('/profileSetting')
def profileSetting():
    if len(session) == 0: return redirect('/login')
    return render_template('Admin/account.htm')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/data')
def viewData():
    if len(session) == 0: return redirect('/login')
    return render_template('Admin/data.htm')

@app.route('/rent')
def viewBookings():
    return render_template('Admin/bookings.htm')

@app.route('/manage')
def manageUsers():
    return render_template('Admin/manageUsers.htm')

@app.route('/report')
def reportView():
    return render_template('Admin/report.htm')




# app.run(host='localhost', port=3000)

if __name__ == '__main__':
    app.run(debug=True)
    