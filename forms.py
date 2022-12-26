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
	number = StringField("Podaj ciąg znaków do hashowania", validators=[DataRequired()])
	submit = SubmitField("Wydrukuj hash")

class TicketForm(FlaskForm):
	name = StringField("Podaj imię osoby, dla której wystawiasz mandat", validators=[DataRequired()])
	surname = StringField("Podaj nazwisko osoby, dla której wystawiasz mandat", validators=[DataRequired()])
	pesel = IntegerField("Podaj pesel osoby, dla której wystawiasz mandat", validators=[DataRequired()]) #dodać walidator po długości
	badge = IntegerField("Podaj numer odznaki funkcjonariusza spisującego mandat", validators=[DataRequired()])
	amount = IntegerField("Podaj wartość mandatu", validators=[DataRequired()])
	pen_points = IntegerField("Podaj liczbę przyznanych punktów karnych", validators=[])
	submit = SubmitField("Zapisz mandat")

class LoginForm(FlaskForm):
	username = StringField("Podaj identyfikator użytkownika", validators=[DataRequired()])
	password= PasswordField("Podaj hasło", validators=[DataRequired()])
	submit = SubmitField("Zaloguj")

class UserForm(FlaskForm):
	username = StringField("Podaj identyfikator", validators=[DataRequired()])
	password_hash = PasswordField("Podaj hasło", validators=[DataRequired(), EqualTo('password_hash2', message='Hasła muszą być identyczne')])
	password_hash2 = PasswordField("Podaj hasło ponownie", validators=[DataRequired()])
	submit = SubmitField("Zarejestruj")
