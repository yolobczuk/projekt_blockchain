# Python application that uses Flask framework to create web app that handles ticketing system for the police

'''
Flask is the micro-web framework, it will be used to show contents of the app in browser
render_template, flash, jsonify, redirect and url_for are all functions that help with displaying the contents in the browser

render_template function renders contents of html file and passes given parameters to it
flash function is responsible for printing messages on pages
jsonify function is responsible for printing the content in json format
redirect and url_for functions work in a similar way - both redirect user to a given page

SQLAlchemy works as a component responsible for maintaining and operating database in Flask
Migrate helps with translating Python classes into tables
the forms file contains all defined forms by us, that will be used in the app
flask_login is responsible for login features (creation of accounts, facilitating logging in to the site and logging out etc.)
werkzeug.security checks whether passwords entered by users are correct
hashlib is used to calculate digital fingerprints of the data
datetime is used to fetch current time
json is used to convert the data before hashing it
'''

from flask import Flask, render_template, flash, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import HashForm, TicketForm, LoginForm, UserForm
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib
import datetime
import json

# Creating the Web app instance using flask
app = Flask(__name__)
app.app_context().push()

# Defining database parameters which simulates the blockchain
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///tickets.db'
app.config['SECRET_KEY'] = "sosecret"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Adding necessary components to handle login features
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Adding database model to store data about the tickets, id column is created automatically and acts as primary key
class Tickets(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	hash = db.Column(db.String(256), nullable = False)
	name = db.Column(db.String(40), nullable = False)
	surname = db.Column(db.String(100), nullable = False)
	pesel = db.Column(db.String(64), nullable = False)
	badge = db.Column(db.String(64), nullable = False)
	amount = db.Column(db.Integer, nullable = False)
	pen_points = db.Column(db.Integer)
	date_added = db.Column(db.DateTime, default = datetime.datetime.utcnow)

	def __repr__(self):
		return '<Name %r>' % self.name

# Adding database model to store blockchain data, hash column is calculated based on block data and acts as primary key
class Block(db.Model):
	hash = db.Column(db.String(256), primary_key = True)
	proof = db.Column(db.Integer, nullable = False)
	previous_hash = db.Column(db.String(256), nullable = False)
	date_added = db.Column(db.DateTime, default = datetime.datetime.utcnow)

	def __repr__(self):
		return '<Hash %r>' % self.hash

# Adding database model to store registered users, id column is created automatically and acts as primary key
# This class also contains functions that handle setting and verifying passwords
class Users(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(20), nullable = False, unique = True)
	date_added = db.Column(db.DateTime, default = datetime.datetime.utcnow)
	password_hash = db.Column(db.String(128))

	@property
	def password(self):
		raise AttributeError("Password is not a readable attribute!")
	
	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return '<Name %r>' % self.name

class Blockchain:
	# This function is created to create the very first block and set its hash to "0"
	# If the block database contains any entries, add them to the chain
	def __init__(self):
		self.chain = []
		self.create_block(proof=1, previous_hash='0', hash = 0)
		blocks = Block.query.order_by(Block.date_added)
		if blocks.count()>1:
			for block in blocks:
				self.create_block(proof=block.proof, previous_hash=block.previous_hash, hash = block.hash)

	# This function is created to add further blocks into the chain
	def create_block(self, proof, previous_hash, hash):
		block = {'index': len(self.chain) + 1,
				'timestamp': str(datetime.datetime.now()),
				'proof': proof,
				'hash': hash,
				'previous_hash': previous_hash}
		self.chain.append(block)
		return block

	# This function is created to display the previous block
	def get_previous_block(self):
		return self.chain[-1]

	# This is the function that creates simple proof of work system which is used to successfully mine the block
	def proof_of_work(self, block):
		hash = self.hash(block)
		while not hash.startswith('0' * 3):
			block['proof'] += 1
			hash = self.hash(block)
		return hash, block['proof']

	# This function calculates digital footprint for a given block
	def hash(self, block):
		encoded_block = json.dumps(block, sort_keys=True).encode()
		return hashlib.sha256(encoded_block).hexdigest()

	# This function checks whether the chain is valid
	def chain_valid(self, chain):
		previous_block = chain[0]
		block_index = 1

		# Checking whether the number of leading zeros is correct and whether previous hash entry actually is the hash of the previous block
		while block_index < len(chain):
			block = chain[block_index]
			if block['previous_hash'] != self.hash(previous_block) or not block['hash'].startswith('0' * 3):
				return False
			previous_block = block
			block_index += 1

		return True

# Create the object of the blockchain class
blockchain = Blockchain()

# Get logged user data
@login_manager.user_loader
def load_user(user_id):
	return Users.query.get(int(user_id))

# This function adds log-in feature to the app
@app.route('/login', methods = ['GET', 'POST'])
def login():
	form = LoginForm()

	# Checking whether the form is submitted
	if form.validate_on_submit():
		user = Users.query.filter_by(username=form.username.data).first()
		
		# Checking whether the user appears in the database
		if user:

			# Checking whether the password matches the one in the database
			if check_password_hash(user.password_hash, form.password.data):
				login_user(user)
				flash("User logged in successfully.")
				return redirect(url_for('index'))
			else:
				flash("Wrong password, please try again.")
		else:
			flash("This user does not exist. Please register first.")
	return render_template('login.html', form = form)

# This function adds registering feature to the app
@app.route('/register', methods = ['GET', 'POST'])
def register():
	form = UserForm()

	# Checking whether the form is submitted
	if form.validate_on_submit():
		user = Users.query.filter_by(username = form.username.data).first()

		# Checking whether the user appears in the database
		if user is None: 
			hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
			user = Users(username = form.username.data, password_hash=hashed_pw)
			db.session.add(user)
			db.session.commit()
		
		# Clearing the form data
		form.username.data = ''
		form.password_hash.data = ''

		flash("User registered successfully")
	return render_template('register.html', form = form)   

# This function adds log-out feature to the app
@app.route('/logout', methods = ['GET', 'POST'])
@login_required
def logout():
	logout_user()
	flash("User logged out successfully")
	return redirect(url_for('login'))

# This function creates welcome page of the site
@app.route('/')
def index():
	return render_template('index.html')

# Add handling of 404 error
@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"), 404

# This function creates page which adds the functionality of printing hash for a given number or string
@app.route('/hash', methods = ['GET', 'POST'])
@login_required
def get_hash():
	hash = None
	number = None
	form = HashForm()

	# Checking whether the form is submitted	
	if form.validate_on_submit():
		number = form.number.data
		form.number.data = None
		hash = hashlib.sha256(str(number).encode()).hexdigest()
		flash("Content has been hashed successfully!")

	return render_template("hash.html", number = number, hash = hash, form = form)

"""
This function serves as the main function of the app, it gives the user ability to fill the ticket.
The function then adds the ticket to the blockchain and saves both block and ticket data to respective databases.
All sensitive information (such as PESEL or badge number) are encrypted by SHA-256 encryption
"""
@app.route('/ticket', methods = ['GET', 'POST'])
@login_required
def fill_ticket():
	form = TicketForm()
	hash = None

	# Checking whether the form is submitted		
	if form.validate_on_submit():
		hashed_pesel = hashlib.sha256(str(form.pesel.data).encode()).hexdigest()
		hashed_badge = hashlib.sha256(str(form.badge.data).encode()).hexdigest()

		block = Block.query.filter_by(hash = hash).first()

		# Checking whether the block exists in the database
		if block is None:

			# Create block
			data = {'name':form.name.data, 'surname':form.surname.data, 'pesel':hashed_pesel,
					'badge' : hashed_badge, 'amount':form.amount.data, 'pen_points' : form.pen_points.data,
					'proof':1,  'timestamp':str(datetime.datetime.now())}

			previous_block = blockchain.get_previous_block()
			hash, data['proof'] = blockchain.proof_of_work(data)
			previous_hash = previous_block['hash']
			blockchain.create_block(proof=data['proof'], hash = hash, previous_hash = previous_hash)

			# Add block data to the database
			block = Block(hash = hash, proof = data['proof'], previous_hash = previous_hash)
			db.session.add(block)
			db.session.commit()

		ticket = Tickets.query.filter_by(hash = hash).first()

		# Checking whether the ticket exists in the database
		if ticket is None:

			# Add ticket data to the database
			ticket = Tickets(hash = hash, name = form.name.data, surname = form.surname.data, pesel = hashed_pesel,
							 badge = hashed_badge, amount=form.amount.data, pen_points = form.pen_points.data)
			db.session.add(ticket)
			db.session.commit()

		# Clearing the form data
		form.name.data = ''
		form.surname.data = ''
		form.pesel.data = ''
		form.badge.data = ''
		form.amount.data = ''
		form.pen_points.data = ''

		flash("Ticket saved successfully!")
	
	# Get both ticket and block database in order to print them on the page
	tickets = Tickets.query.order_by(Tickets.date_added)
	blocks = Block.query.order_by(Block.date_added)
	return render_template('ticket.html', form = form, tickets=tickets, blocks = blocks)

# This function creates page which that prints ticket data for a given hash of a block
# The hash parameter is required - it acts as a filter that has to be applied to a database in order to obtain the specific data
@app.route('/ticket/<hash>', methods = ['GET', 'POST'])
@login_required
def get_data(hash):
	ticket_to_print = Tickets.query.filter_by(hash = hash).first()
	return render_template("details.html", 
			ticket_to_print = ticket_to_print, hash = hash)

# This function creates page which that prints ticket data for a given PESEL hash
# The hash parameter is required - it acts as a filter that has to be applied to a database in order to obtain the specific data
@app.route('/ticket/details/<hash>', methods = ['GET', 'POST'])
@login_required
def get_pesel_data(hash):
	tickets_to_print = Tickets.query.filter_by(pesel = hash).order_by(Tickets.date_added)
	init_info = Tickets.query.filter_by(pesel = hash).first()
	if tickets_to_print.count() > 0:
		return render_template("details_pesel.html", 
				tickets = tickets_to_print, pesel = init_info.pesel, imie = init_info.name, nazwisko = init_info.surname)
	else:
		return render_template("details_pesel.html", hash = hash)

# This function creates page which that prints ticket data for a given badge number hash
# The hash parameter is required - it acts as a filter that has to be applied to a database in order to obtain the specific data
@app.route('/ticket/policeman/<hash>', methods = ['GET', 'POST'])
@login_required
def get_badge_data(hash):
	tickets_to_print = Tickets.query.filter_by(badge = hash).order_by(Tickets.date_added)
	init_info = Tickets.query.filter_by(badge = hash).first()
	if tickets_to_print.count() > 0:
		return render_template("details_badge.html", 
				tickets = tickets_to_print, badge = init_info.badge)
	else:
		return render_template("details_badge.html", hash = hash)

# This function creates page which that prints all tickets data, with no filter
@app.route('/ticket/all', methods = ['GET', 'POST'])
@login_required
def get_all_tickets():
	blocks = Block.query.order_by(Block.date_added)
	return render_template("all_tickets.html", 
			blocks = blocks)


# Mining a new block
@app.route('/mine_block', methods=['GET'])
def mine_block():
	previous_block = blockchain.print_previous_block()
	previous_proof = previous_block['proof']
	proof = blockchain.proof_of_work(previous_proof)
	previous_hash = blockchain.hash(previous_block)
	block = blockchain.create_block(proof, previous_hash)

	response = {'message': 'A block is MINED',
				'index': block['index'],
				'timestamp': block['timestamp'],
				'proof': block['proof'],
				'previous_hash': block['previous_hash']}

	return jsonify(response), 200

# Check validity of blockchain
@app.route('/valid', methods=['GET'])
def valid():
	valid = blockchain.chain_valid(blockchain.chain)

	if valid:
		response = {'message': 'The Blockchain is valid.'}
	else:
		response = {'message': 'The Blockchain is not valid.'}
	return jsonify(response), 200


# Run the flask server locally
app.run(host='127.0.0.1', port=8080)