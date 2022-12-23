# Python program to create Blockchain

# For timestamp
import datetime

# Calculating the hash
# in order to add digital
# fingerprints to the blocks
# import hashlib

# To store data
# in our blockchain
import json

# Flask is for creating the web
# app and jsonify is for
# displaying the blockchain
from flask import Flask, render_template, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import HashForm, TicketForm
import hashlib

class Blockchain:
	# This function is created
	# to create the very first
	# block and set its hash to "0"
	def __init__(self):
		self.chain = []
		self.create_block(proof=1, previous_hash='0', hash = 0, data=['Genesis block'])

	# This function is created
	# to add further blocks
	# into the chain
	def create_block(self, proof, previous_hash, hash, data):
		block = {'index': len(self.chain) + 1,
				'timestamp': str(datetime.datetime.now()),
				'proof': proof,
				'hash': hash,
				'data': data,
				'previous_hash': previous_hash}
		self.chain.append(block)
		return block

	# This function is created
	# to display the previous block
	def get_previous_block(self):
		return self.chain[-1]

	# This is the function for proof of work
	# and used to successfully mine the block
	def proof_of_work(self, block):
		hash = self.hash(block)
		while not hash.startswith('0' * 3):
			block['proof'] += 1
			hash = self.hash(block)
		return hash, block['proof']

	def hash(self, block):
		encoded_block = json.dumps(block, sort_keys=True).encode()
		return hashlib.sha256(encoded_block).hexdigest()

	def chain_valid(self, chain):
		previous_block = chain[0]
		block_index = 1

		while block_index < len(chain):
			block = chain[block_index]
			if block['previous_hash'] != self.hash(previous_block) or not block['hash'].startswith('0' * 3):
				return False
			previous_block = block
			block_index += 1

		return True

# Creating the Web
# App using flask


app = Flask(__name__)


app.app_context().push()

# Create the object
# of the class blockchain
blockchain = Blockchain()

# Defining database which
# simulates the blockchain
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///tickets.db'
app.config['SECRET_KEY'] = "sosecret"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Add temporary database model
# to store data about the tickets
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

# Add temporary database model
# to store blockchain data
class Block(db.Model):
	hash = db.Column(db.String(256), primary_key = True)
	proof = db.Column(db.Integer, nullable = False)
	previous_hash = db.Column(db.String(256), nullable = False)
	date_added = db.Column(db.DateTime, default = datetime.datetime.utcnow)

	def __repr__(self):
		return '<Hash %r>' % self.hash

if Block.query.order_by(Block.date_added).count()==0:
	blockchain.initialise()

# Create main page of the site
@app.route('/')
def index():
	return render_template('index.html')

# Add handling of 404 error
@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"), 404

# Create page which
# will add the functionality
# of printing hash for
# a given number or string
@app.route('/hash', methods = ['GET', 'POST'])
def get_hash():
	hash = None
	number = None
	form = HashForm()

	if form.validate_on_submit():

		number = form.number.data
		form.number.data = None
		hash = hashlib.sha256(str(number).encode()).hexdigest()
		flash("Numer zahashowany pomyślnie!")

	return render_template("hash.html", number = number, hash = hash, form = form)
# Create page which
# will serve as main
# point of the site.
# It gives the ability
# to fill out the ticket data
@app.route('/ticket', methods = ['GET', 'POST'])
def fill_ticket():
	form = TicketForm()
	hash = None
	if form.validate_on_submit():
		hashed_pesel = hashlib.sha256(str(form.pesel.data).encode()).hexdigest()
		hashed_badge = hashlib.sha256(str(form.badge.data).encode()).hexdigest()

		block = Block.query.filter_by(hash = hash).first()
		if block is None:
			data = {'name':form.name.data, 'surname':form.surname.data, 'pesel':hashed_pesel,
					'badge' : hashed_badge, 'amount':form.amount.data, 'pen_points' : form.pen_points.data,
					'proof':1}

			previous_block = blockchain.get_previous_block()
			hash, data['proof'] = blockchain.proof_of_work(data)
			previous_hash = previous_block['hash']
			blockchain.create_block(proof=data['proof'], hash = hash, previous_hash = previous_hash, data = data)
			block = Block(hash = hash, proof = data['proof'], previous_hash = previous_hash)
			db.session.add(block)
			db.session.commit()

		ticket = Tickets.query.filter_by(name = form.name.data).first()
		if ticket is None:
			ticket = Tickets(hash = hash, name = form.name.data, surname = form.surname.data, pesel = hashed_pesel,
							 badge = hashed_badge, amount=form.amount.data, pen_points = form.pen_points.data)
			db.session.add(ticket)
			db.session.commit()

		form.name.data = ''
		form.surname.data = ''
		form.pesel.data = ''
		form.badge.data = ''
		form.amount.data = ''
		form.pen_points.data = ''

		flash("Mandat zapisany pomyślnie!")
	tickets = Tickets.query.order_by(Tickets.date_added)
	blocks = Block.query.order_by(Block.date_added)
	return render_template('ticket.html', form = form, tickets=tickets, blocks = blocks)

@app.route('/ticket/<hash>', methods = ['GET', 'POST'])
def get_data(hash):
	ticket_to_print = Tickets.query.filter_by(hash = hash).first()
	return render_template("details.html", 
			ticket_to_print = ticket_to_print)

@app.route('/ticket/details/<hash>', methods = ['GET', 'POST'])
def get_pesel_data(hash):
	tickets_to_print = Tickets.query.filter_by(pesel = hash)
	init_info = tickets_to_print.first()
	return render_template("details_pesel.html", 
			ticket_to_print = tickets_to_print, pesel = init_info.pesel, imie = init_info.name, nazwisko = init_info.surname)

@app.route('/ticket/policeman/<hash>', methods = ['GET', 'POST'])
def get_badge_data(hash):
	tickets_to_print = Tickets.query.filter_by(badge = hash)
	init_info = tickets_to_print.first()
	return render_template("details_badge.html", 
			ticket_to_print = tickets_to_print, badge = init_info.badge)


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