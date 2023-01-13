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
	number = StringField("Insert text/number which you would like to hashcode", validators=[DataRequired()])
	submit = SubmitField("Print hashcode")

class TicketForm(FlaskForm):
	name = StringField("Name of the person who received a ticket", validators=[DataRequired()])
	surname = StringField("Surname of the person who received a ticket", validators=[DataRequired()])
	pesel = IntegerField("PESEL of the person who received a ticket", validators=[DataRequired()]) #dodać walidator po długości
	badge = IntegerField("Badge number of the policeman who gave a ticket", validators=[DataRequired()])
	amount = IntegerField("Fine amount", validators=[DataRequired()])
	pen_points = IntegerField("Penalty points given (PLN)", validators=[])
	submit = SubmitField("Save ticket")

class LoginForm(FlaskForm):
	username = StringField("User name", validators=[DataRequired()])
	password= PasswordField("Password", validators=[DataRequired()])
	submit = SubmitField("Log in")

class UserForm(FlaskForm):
	username = StringField("User name", validators=[DataRequired()])
	password_hash = PasswordField("Password", validators=[DataRequired(), EqualTo('password_hash2', message='Hasła muszą być identyczne')])
	password_hash2 = PasswordField("Retype password", validators=[DataRequired()])
	submit = SubmitField("Register")
