from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.htm')

@app.route('/login')
def loginForm():
    return render_template('login.htm')

@app.route('/about')
def aboutView():
    return render_template('about.htm')

@app.route('/books')
def serviceView():
    return render_template('service.htm')

@app.route('/dashboard')
def dashboard():
    return render_template('Admin/index.htm')

@app.route('/profileSetting')
def profileSetting():
    return render_template('Admin/account.htm')

@app.route('/logout')
def logout():
    return render_template('login.htm')

@app.route('/data')
def viewData():
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

if __name__ == '__main__':
    app.run(debug=True)
    