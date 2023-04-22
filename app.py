from flask import Flask, render_template, request, session, redirect
import mysql.connector
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import os

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
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

mycursor = mydb.cursor()

@app.route('/')
def index():
    return render_template('index.htm')

# user login validations
@app.route('/login')
def loginForm():
    return render_template('login.htm')

@app.route('/signin', methods=['POST'])
def login_post():
    #? Get form data and data validation
    username = request.form['username']
    password = request.form['password']
    
    mycursor.execute("SELECT * FROM users WHERE username = %s", [username])
    users = mycursor.fetchall()
    if users: 
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

# dashboard manipulations
@app.route('/dashboard')
def dashboard():
    if len(session) == 0: return render_template('login.htm',error='You must login First')
    user = session['user_id']
    return render_template('Admin/index.htm',user = user)

# user profile setings
@app.route('/profileSetting')
def profileSetting():
    if len(session) == 0: return render_template('login.htm',error='You must login First')
    return render_template('Admin/account.htm')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# books
@app.route('/data')
def viewData():
    if len(session) == 0: return render_template('login.htm',error='You must login First')
    mycursor.execute("SELECT *FROM books")
    data = mycursor.fetchall()
    return render_template('Admin/data.htm',data=data)

@app.route('/addBook',methods=['POST'])
def addBook():
    # form data
    title = request.form['title']
    author = request.form['author']
    publisher = request.form['publisher']
    quantity = request.form['quantity']
    file = request.files['image']
    filename = file.filename
    file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
    sql = "INSERT INTO `books`(`title`, `auth`, `quantity`, `publisher`, `image`) VALUES (%s,%s,%s,%s,%s)"
    res = mycursor.execute(sql,(title,author,quantity,publisher,filename))
    mydb.commit()
    if res:
        status = "Data inserted Successfully!"
        return render_template('Admin/data.htm',status=status)
    return redirect('/data')

# bookings
@app.route('/rent')
def viewBookings():
    if len(session) == 0: return render_template('login.htm',error='You must login First')
    mycursor.execute("SELECT *FROM bookings")
    data = mycursor.fetchall()
    return render_template('Admin/bookings.htm',data=data)

# reports 
@app.route('/report')
def reportView():
    if len(session) == 0: return render_template('login.htm',error='You must login First')
    return render_template('Admin/report.htm')

# admin data manipulations routes

@app.route('/manage')
def manageUsers():
    if len(session) == 0: return render_template('login.htm',error='You must login First')
    mycursor.execute("SELECT * FROM users WHERE status=1")
    data = mycursor.fetchall()
    return render_template('Admin/manageUsers.htm',data=data)

@app.route('/user/delete/<int:id>')
def deleteUser(id):
    id = str(id)
    if len(session) == 0: return render_template('login.htm',error='You must login First')
    # query = "DELETE FROM users WHERE id ="+id+""
    query = "UPDATE `users` SET `status` = '0' WHERE id ="+id+""
    mycursor.execute(query)
    mydb.commit()
    return redirect('/manage')


@app.route('/register',methods=['GET','POST'])
def store():
    fname = request.form['firstName']
    lname = request.form['lastName']
    email = request.form['email']
    password = request.form['password']
    passd = generate_password_hash(password)
    uid = request.form['id']
    sql = "INSERT INTO `users`(`fname`, `lname`, `username`, `password`, `pid`) VALUES (%s,%s,%s,%s,%s)"
    res = mycursor.execute(sql,(fname,lname,email,passd,uid))
    mydb.commit()
    if res:
        status = "Data inserted Successfully!"
        return render_template('Admin/manageUsers.htm',status=status)
    return redirect('/manage')

# app.run(host='localhost', port=3000)

if __name__ == '__main__':
    app.run(debug=True)
    