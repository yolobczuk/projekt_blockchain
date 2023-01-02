'''
This file is responsible for creation of forms used in the web app
flask_wtf is the framework that handles the forms, FlaskForm is the class of the form used in Flask frameword
wtforms adds some functionalitites to the forms

StringField, SubmitField, IntegerField and PasswordField are all types of the fields in forms
They accept the string that acts as label for a given field

validators check whether the data written in the form is correct by some of the constraints
We used two validators - DataRequired (user has to fill the field) and EqualTo (the field contents must be equal to another)
'''

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, PasswordField
from wtforms.validators import DataRequired, EqualTo

class HashForm(FlaskForm):
	number = StringField("Enter a string to hash", validators=[DataRequired()])
	submit = SubmitField("Print the hash")

class TicketForm(FlaskForm):
	name = StringField("Enter the first name of the person, that you are issuing the ticket for", validators=[DataRequired()])
	surname = StringField("Enter the last name of the person, that you are issuing the ticket for", validators=[DataRequired()])
	pesel = IntegerField("Enter the PESEL of the person, that you are issuing the ticket for", validators=[DataRequired()]) #dodać walidator po długości
	badge = IntegerField("Enter the badge number of the officer who is issuing the ticket", validators=[DataRequired()])
	amount = IntegerField("Enter ticket value", validators=[DataRequired()])
	pen_points = IntegerField("Enter the number of penalty points", validators=[])
	submit = SubmitField("Save the ticket")

class LoginForm(FlaskForm):
	username = StringField("Enter the ID of the user", validators=[DataRequired()])
	password= PasswordField("Enter the password", validators=[DataRequired()])
	submit = SubmitField("Log in")

class UserForm(FlaskForm):
	username = StringField("Enter ID", validators=[DataRequired()])
	password_hash = PasswordField("Enter the password", validators=[DataRequired(), EqualTo('password_hash2', message='Hasła muszą być identyczne')])
	password_hash2 = PasswordField("Repeat the password", validators=[DataRequired()])
	submit = SubmitField("Sign in")
