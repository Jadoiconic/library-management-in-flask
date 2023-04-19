from flask import Flask, render_template, request, session, redirect
import mysql.connector
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)


#! Configure MySQL connection
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="library"
)

app.config['SECRET_KEY'] = 'your_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60)

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
    mycursor.execute("SELECT * FROM users WHERE username = %s", [username])
    users = mycursor.fetchall()
    
    if users:
        #? Store the user ID in a session variable
        userPass = users[0][4]
        if check_password_hash(userPass, password):
            session['user_id'] = list(users)
            return redirect('/dashboard')
        else:
            return render_template('login.htm', error='Incorect Password!')
            
    else:
        return render_template('login.htm', error='User Not found!')
    
    
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
    if len(session) == 0: return render_template('login.htm',error='You must login First')
    return render_template('Admin/account.htm')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/data')
def viewData():
    if len(session) == 0: return render_template('login.htm',error='You must login First')
    return render_template('Admin/data.htm')

@app.route('/rent')
def viewBookings():
    if len(session) == 0: return render_template('login.htm',error='You must login First')
    return render_template('Admin/bookings.htm')

@app.route('/manage')
def manageUsers():
    if len(session) == 0: return render_template('login.htm',error='You must login First')
    mycursor.execute("SELECT * FROM users")
    data = mycursor.fetchall()
    return render_template('Admin/manageUsers.htm',data=data)

@app.route('/report')
def reportView():
    if len(session) == 0: return render_template('login.htm',error='You must login First')
    return render_template('Admin/report.htm')

# admin data manipulations routes

@app.route('/register',methods=['GET','POST'])
def store():
    fname = request.form['firstName']
    lname = request.form['lastName']
    email = request.form['email']
    password = request.form['password']
    passd = generate_password_hash(password)
    uid = request.form['id']
    sql = "INSERT INTO `users`(`fname`, `lname`, `username`, `password`, `pid`) VALUES (%s,%s,%s,%s,%s)"
    mycursor.execute(sql,(fname,lname,email,passd,uid))
    mydb.commit()
    return render_template('Admin/manageUsers.htm',error = 'Data inserted Successfully!')

# app.run(host='localhost', port=3000)

if __name__ == '__main__':
    app.run(debug=True)
    