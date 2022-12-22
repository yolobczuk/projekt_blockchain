# Python program to create Blockchain

# For timestamp
import datetime

# Calculating the hash
# in order to add digital
# fingerprints to the blocks
import hashlib

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
		self.create_block(proof=1, previous_hash='0',data=['Genesis block'])

	# This function is created
	# to add further blocks
	# into the chain
	def create_block(self, proof, previous_hash, data):
		block = {'index': len(self.chain) + 1,
				'timestamp': str(datetime.datetime.now()),
				'proof': proof,
				'data': data,
				'previous_hash': previous_hash}
		self.chain.append(block)
		return block

	# This function is created
	# to display the previous block
	def print_previous_block(self):
		return self.chain[-1]

	# This is the function for proof of work
	# and used to successfully mine the block
	def proof_of_work(self, previous_proof):
		new_proof = 1
		check_proof = False

		while check_proof is False:
			hash_operation = hashlib.sha256(
				str(new_proof**2 - previous_proof**2).encode()).hexdigest()
			if hash_operation[:5] == '00000':
				check_proof = True
			else:
				new_proof += 1

		return new_proof

	def hash(self, block):
		encoded_block = json.dumps(block, sort_keys=True).encode()
		return hashlib.sha256(encoded_block).hexdigest()

	def chain_valid(self, chain):
		previous_block = chain[0]
		block_index = 1

		while block_index < len(chain):
			block = chain[block_index]
			if block['previous_hash'] != self.hash(previous_block):
				return False

			previous_proof = previous_block['proof']
			proof = block['proof']
			hash_operation = hashlib.sha256(
				str(proof**2 - previous_proof**2).encode()).hexdigest()

			if hash_operation[:5] != '00000':
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
def get_ticket():
	form = TicketForm()
	hashed_pesel = None

	if form.validate_on_submit():
		ticket = Tickets.query.filter_by(badge = form.badge.data).first()
		if ticket is None: 
			hashed_pesel = hashlib.sha256(str(form.pesel.data).encode()).hexdigest()
			hashed_badge = hashlib.sha256(str(form.badge.data).encode()).hexdigest()
			ticket = Tickets(name = form.name.data, surname = form.surname.data, pesel = hashed_pesel, badge = hashed_badge, amount=form.amount.data, pen_points = form.pen_points.data)
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
	return render_template('ticket.html', form = form, pesel = hashed_pesel, tickets=tickets)  

# Add temporary database model
# to store data about the tickets
class Tickets(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(40), nullable = False)
	surname = db.Column(db.String(100), nullable = False)
	pesel = db.Column(db.String(64), nullable = False)
	badge = db.Column(db.String(64), nullable = False)
	amount = db.Column(db.Integer, nullable = False)
	pen_points = db.Column(db.Integer)
	date_added = db.Column(db.DateTime, default = datetime.datetime.utcnow)

	def __repr__(self):
		return '<Name %r>' % self.name

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

# Display blockchain in json format


@app.route('/get_chain', methods=['GET'])
def display_chain():
	response = {'chain': blockchain.chain,
				'length': len(blockchain.chain)}
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
# app.run(host='127.0.0.1', port=5000)