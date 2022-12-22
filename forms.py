from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired

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