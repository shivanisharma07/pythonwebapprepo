from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy 
import os
import hashlib 

app = Flask(__name__)
app.secret_key = "Secret Key"

path = os.path.abspath( os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(path , 'database.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Crud(db.Model):
	id = db.Column(db.Integer , primary_key = True)
	name = db.Column(db.String(100))
	email = db.Column(db.String(100))
	coursecode = db.Column(db.String(100))	
	rollno 	= db.Column(db.Integer)
	coursename = db.Column(db.String(100))
	startdate = db.Column(db.String(100))
	enddate	  = db.Column(db.String(100))
	datahash  = db.Column(db.String(100))
	bctransactionno =  db.Column(db.String(150))
	
	def __init__(self, name, email, coursecode, rollno , coursename,startdate,enddate,datahash ) :
		self.name 	= name
		self.email 	= email
		self.coursecode = coursecode
		self.rollno 	= rollno
		self.coursename = coursename
		self.startdate	=	startdate
		self.enddate	=	enddate
		self.datahash	=	datahash
		#self.bctransactionno = bctransactionno


@app.route('/')
def index():
    all_data = Crud.query.all()
    return render_template("index.html", all_data = all_data)

@app.route('/insert', methods = ['POST'])
def insert():
	if request.method == 'POST':
		name 	= request.form['name']
		email 	= request.form['email']
		coursecode 	= request.form['coursecode']
		coursename 	= request.form['coursename']
		rollno		= request.form['rollno']
		startdate	=	request.form["startdate"]
		enddate		=	request.form["enddate"]

		finalstr 	= 	name.strip()+ email.strip() + coursecode.strip() + coursename.strip()
		finalstr	=	finalstr + rollno.strip() + startdate.strip() + enddate.strip()
		datahash	=	 hashlib.md5(finalstr.encode()).hexdigest()  
		my_data = Crud(name, email, coursecode, rollno , coursename,startdate,enddate,datahash)
		db.session.add(my_data)
		db.session.commit()

		dstr 	= 	coursecode.strip() +','+ rollno.strip() +','+ name.strip()+','+  coursename.strip()
		dstr	=	dstr +',' +email.strip()+',' +  startdate.strip() +','+ enddate.strip()+','+ datahash.strip()

		flash("Data Inserted Successfully :  "+dstr)
		return redirect(url_for('index'))

@app.route('/update', methods = ['POST'])
def update():
    if request.method == "POST":
        my_date = Crud.query.get(request.form.get('id'))
        #my_date.name = request.form['name']
        #my_date.email = request.form['email']
        my_date.bctransactionno = request.form['bctransactionno']

        db.session.commit()
        flash("Transaction ID updated Successfully")
        return redirect(url_for('index'))

@app.route('/viewbc' )
def viewbc():
		bctx ="0x2a4959784f7c3a4090c154a83f45c3bd3658295fa7e250c55803088df99c4344"
		return redirect("https://rinkeby.etherscan.io/tx/"+bctx)
	
		
@app.route('/delete/<id>/')
def delete(id):
    my_data = Crud.query.get(id)
    db.session.delete(my_data)
    db.session.commit()

    flash("student Data Deleted Successfully")
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug = True)

