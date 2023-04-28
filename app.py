from flask import Flask, render_template, request, session, redirect, url_for,flash
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
    
    mycursor.execute("SELECT * FROM users WHERE username = %s AND status=1", [username])
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

#client bookings
@app.route('/books')
def serviceView():
    mycursor.execute("SELECT *FROM books WHERE status='1'")
    data = mycursor.fetchall()
    return render_template('service.htm',data=data)

# manipulate data for borrowing book
@app.route('/borrow',methods=['GET','POST'])
def borrowBook():
    id = request.form['id']
    fname = request.form['firstName']
    lname = request.form['lastName']
    names = fname+" "+ lname
    phone = request.form['phone']
    address = request.form['address']
    email = request.form['email']
    
    mycursor.execute("SELECT *FROM books WHERE status='1' AND bookId="+id)
    data = mycursor.fetchall()
    print(data)
    data = data[0][3]
    if data > 0: 
        mycursor.execute("UPDATE books SET quantity=quantity-1 WHERE status='1' AND bookId="+id)
        qry = "INSERT INTO `bookings`(`names`, `bookId`, `address`, `phone`, `email`) VALUES (%s,%s,%s,%s,%s)"
        mycursor.execute(qry,(names,id,address,phone,email))
        mydb.commit()
        flash('Your Request Sent!')
        return redirect(url_for('serviceView'))
    else:
        return "No books available!"

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

# change password for current user
@app.route('/change-password',methods=['GET','POST'])
def changePassword():
    passd = session['user_id'][0][4]
    uid = str(session['user_id'][0][0])
    fpass = request.form['cpassword']
    npass = request.form['password']
    cnpass = request.form['repassword']
    if check_password_hash(passd,fpass) :
        if npass == cnpass:
            password = generate_password_hash(npass)
            query = "UPDATE `users` SET `password` ='"+password+"' WHERE id ="+uid+""
            mycursor.execute(query)
            flash('Password have been changed!')
            return redirect(url_for('logout'))
        else:
            flash('Password Does not match!')
            return redirect(url_for('profileSetting'))
    else:
        flash('Your current Password is incorrect Try again!')
        return redirect(url_for('profileSetting'))


# logon out method
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# books
@app.route('/data')
def viewData():
    if len(session) == 0: return render_template('login.htm',error='You must login First')
    mycursor.execute("SELECT *FROM books WHERE status='1' ORDER BY bookid DESC")
    data = mycursor.fetchall()
    return render_template('Admin/data.htm',data=data)

@app.route('/addBook',methods=['POST'])
def addBook():
    # form data
    if len(session) == 0: return render_template('login.htm',error='You must login First')
    title = request.form['title']
    author = request.form['author']
    publisher = request.form['publisher']
    quantity = request.form['quantity']
    file = request.files['image']
    filename = file.filename
    uid = str(session['user_id'][0][0])
    file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
    sql = "INSERT INTO `books`(`title`, `auth`, `quantity`, `publisher`, `image`,`uid`) VALUES (%s,%s,%s,%s,%s,%s)"
    mycursor.execute(sql,(title,author,quantity,publisher,filename,uid))
    mydb.commit()
    flash("Book have been added Successfully!")
    return redirect('/data')
# editng and updating books

@app.route('/book/edit/<int:id>')
def editBook(id):
    id = str(id)
    mycursor.execute("SELECT *FROM books WHERE bookid="+id+"")
    data = mycursor.fetchall()
    return render_template('Admin/editBook.htm', data= data[0])

# handle Update Book
@app.route('/handleUpdateBook',methods=['POST'])
def handleUpdateBook():
    id = request.form['id']
    author = request.form['author']
    desc = request.form['publisher']
    quantity = request.form['quantity']
    title = request.form['title']
    query = "UPDATE `books` SET `title` ='"+title+"',`auth` ='"+author+"',`quantity` ='"+quantity+"',`publisher` ='"+desc+"'  WHERE bookId ="+id+""
    mycursor.execute(query)
    mydb.commit()
    flash('Book have been Updated!')
    return redirect(url_for('viewData'))


# deleting books
@app.route('/book/delete/<int:id>')
def deleteBooks(id):
    id = str(id)
    
    if len(session) == 0: return render_template('login.htm',error='You must login First')
    # query = "DELETE FROM users WHERE id ="+id+""
    
    
    query = "UPDATE `books` SET `status` = '0' WHERE bookId ="+id+""
    mycursor.execute(query)
    mydb.commit()
    flash('Book have been deleted!')
    return redirect('/data')

# bookings
@app.route('/rent')
def viewBookings():
    if len(session) == 0: return render_template('login.htm',error='You must login First')
    mycursor.execute("SELECT *FROM bookings,books WHERE `bookings`.`bookId`=`books`.`bookId` ORDER BY bookings.id DESC")
    data = mycursor.fetchall()
    # return data 
    return render_template('Admin/bookings.htm',data=data)

# approve bookings
@app.route('/rent/approve/<int:id>')
def approveBooking(id):
    id = str(id)
    query = "UPDATE `bookings` SET `status` = '1', `updatedAt` =current_timestamp()  WHERE id ="+id+""
    mycursor.execute(query)
    mydb.commit()
    flash('You have approved this record!')
    return redirect(url_for('viewBookings'))

# reports 
@app.route('/report')
def reportView():
    if len(session) == 0: return render_template('login.htm',error='You must login First')
    # selecting rent books
    mycursor.execute("SELECT *FROM bookings,books WHERE `bookings`.`bookId`=`books`.`bookId` ORDER BY bookings.id DESC")
    booked = mycursor.fetchall()
    # select books
    mycursor.execute("SELECT *FROM books WHERE status='1' ")
    books = mycursor.fetchall()
    n=1
    return render_template('Admin/report.htm',booked=booked, books = books, n=n+1)

# admin data manipulations routes
@app.route('/manage')
def manageUsers():
    if len(session) == 0: return render_template('login.htm',error='You must login First')
    mycursor.execute("SELECT * FROM users WHERE status=1 ORDER BY id DESC")
    data = mycursor.fetchall()
    return render_template('Admin/manageUsers.htm',data=data)

@app.route('/user/delete/<int:id>')
def deleteUser(id):
    id = str(id)
    if len(session) == 0: return render_template('login.htm',error='You must login First')
    # query = "DELETE FROM users WHERE id ="+id+""
    if str(session['user_id'][0][0]) == id: 
        flash('You can\'t Delete your accout!')
        return redirect('/manage')
    else:
        query = "UPDATE `users` SET `status` = '0' WHERE id ="+id+""
        mycursor.execute(query)
        mydb.commit()
        return redirect('/manage')

# update user
@app.route('/user/edit/<int:id>')
def editUser(id):
    id = str(id)
    if len(session) == 0: return render_template('login.htm',error='You must login First')
    mycursor.execute("SELECT * FROM users WHERE id='"+id+"'")
    data = mycursor.fetchall()
    return render_template('Admin/editUsers.htm',data=data[0])

# handle update user
@app.route('/updateuser',methods=['GET','POST'])
def handleUpdateUser():
    if len(session) == 0: return render_template('login.htm',error='You must login First')
    id = request.form['id']
    fname = request.form['firstName']
    lname = request.form['lastName']
    email = request.form['email']
    ident = request.form['identinty']
    query = "UPDATE `users` SET `fname` = '"+fname+"',`lname` = '"+lname+"',`username` = '"+email+"',`pid` = '"+ident+"',`updatedAt` = current_timestamp() WHERE id ="+id+""
    mycursor.execute(query)
    mydb.commit()
    flash('User Updated Successfly!')
    return redirect(url_for('manageUsers'))

# create user
@app.route('/register',methods=['GET','POST'])
def store():
    if len(session) == 0: return render_template('login.htm',error='You must login First')
    fname = request.form['firstName']
    lname = request.form['lastName']
    email = request.form['email']
    password = request.form['password']
    passd = generate_password_hash(password)
    uid = request.form['id']
    sql = "INSERT INTO `users`(`fname`, `lname`, `username`, `password`, `pid`) VALUES (%s,%s,%s,%s,%s)"
    mycursor.execute(sql,(fname,lname,email,passd,uid))
    mydb.commit()
    flash("Data inserted Successfully!")
    return redirect('/manage')

# app.run(host='localhost', port=3000)
if __name__ == '__main__':
    app.run(debug=True)
