from flask_wtf import FlaskForm
from wtforms import DateField, SubmitField, SelectField
from wtforms.validators import DataRequired
import requests
from datetime import datetime


link = 'https://api.nbp.pl/api/exchangerates/tables/a'
currencies = requests.get(link).json()[0]['rates']
curr_codes = ['Wybierz walutę'] + [curr['code'] for curr in currencies]


class EconomyForm(FlaskForm):
    currency1 = SelectField(choices=curr_codes, validators=[DataRequired()])
    currency2 = SelectField(choices=curr_codes, validators=[DataRequired()])
    currency3 = SelectField(choices=curr_codes, validators=[DataRequired()])
    startdate = DateField(default=datetime.today, validators=[DataRequired()], label='Od')
    todate = DateField(default=datetime.today, validators=[DataRequired()], label='Do')
    submit = SubmitField('Sprawdź')