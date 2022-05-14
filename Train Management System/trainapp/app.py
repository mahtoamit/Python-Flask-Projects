from flask import Flask,session,render_template
import database as db
import pymysql
import re 
con = pymysql.connect(host = 'localhost', user = 'root', password = '', database = 'train')
cursor = con.cursor()


app = Flask(__name__)
app.secret_key = 'cairocoders-ednalan'

@app.route('/')
def index():                #homepage
    # Check if user is loggedin
    if 'loggedin' in session:
   
        # User is loggedin show them the home page
        return render_template('index.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route("/ticketform")
def ticketform():
    return render_template("ticketform.html")

@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
  
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if req.method == 'POST' and 'username' in req.form and 'password' in req.form:
        # Create variables for easy access
        username = req.form['username']
        password = req.form['password']
        # Check if account exists using MySQL
        cursor.execute('SELECT * FROM account WHERE username = %s AND password = %s', (username, password))
        # Fetch one record and return result
        acc = cursor.fetchone()
   
    # If acc exists in account table in out database
        if acc:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = acc[0]
            session['username'] = acc[2]
            # Redirect to home page
            #return 'Logged in successfully!'
            return redirect(url_for('index'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    
    return render_template('login.html', msg=msg)

@app.route('/register', methods=['GET', 'POST'])
def register():
 
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if req.method == 'POST' and 'username' in req.form and 'password' in req.form and 'email' in req.form:
        # Create variables for easy access
        fullname = req.form['fullname']
        username = req.form['username']
        password = req.form['password']
        email = req.form['email']
   
  #Check if account exists using MySQL
        cursor.execute('SELECT * FROM account WHERE username = %s', (username))
        acc = cursor.fetchone()
        # If account exists show error and validation checks
        if acc:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO account VALUES (NULL, %s, %s, %s, %s)', (fullname, username, password, email)) 
            con.commit()
   
            msg = 'You have successfully registered!'
    elif req.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)
  
    
@app.route("/passengerlist")
def passengerlist():
    plist = db.all()
    return render_template("passengerlist.html",plist=plist)


from flask import url_for, redirect
@app.route("/passengerdelete/<int:pnrno>")
def deletepassenger(pnrno):
    db.delete(pnrno)
    return redirect(url_for("passengerlist"))

from flask import request as req
@app.route("/passengeradd", methods=['POST','GET'])
def passengeradd():
    if req.method=='GET':
        return render_template("addpassengers.html")
    elif req.method=='POST':
        name = req.form["pname"]
        agee = req.form["age"]
        trainno = req.form["ptrainno"]
        trainname = req.form["ptrainname"]
        classs = req.form["pclass"]
        sour = req.form["psource"]
        dest = req.form["pdest"]
        amt = req.form["pamt"]
        status = req.form["pstatus"]
        doj = req.form["pdoj"]

        db.insert(pname=name,age=agee,ptrainno=trainno,ptrainname=trainname,pclass=classs,psource=sour,pdest=dest,pamt=amt,pstatus=status,pdoj=doj)
        return redirect(url_for("passengerlist"))

@app.route("/passengerupdate/<int:pnrno>", methods=['POST','GET'])
def updatepassenger(pnrno):
        if req.method=='GET':
            passenger=db.get_single_passenger(pnrno=pnrno)
            return render_template("updatepassengers.html",passenger=passenger)

        elif req.method=='POST':
            name = req.form["pname"]
            agee = req.form["age"]
            trainno = req.form["ptrainno"]
            trainname = req.form["ptrainname"]
            classs = req.form["pclass"]
            sour = req.form["psource"]
            dest = req.form["pdest"]
            amt = req.form["pamt"]
            status = req.form["pstatus"]
            doj = req.form["pdoj"]

            db.update(pname=name,age=agee,ptrainno=trainno,ptrainname=trainname,pclass=classs,psource=sour,pdest=dest,pamt=amt,pstatus=status,pdoj=doj,pnrno=pnrno)
            return redirect(url_for("passengerlist"))




if __name__ == '__main__':
    app.run(debug=True)
