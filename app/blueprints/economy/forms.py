from flask_wtf import FlaskForm
from wtforms import DateField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length
import requests
from datetime import datetime


link = 'https://api.nbp.pl/api/exchangerates/tables/A'
currencies = requests.get(link).json()[0]['rates']
curr_codes = [curr['code'] for curr in currencies]


class EconomyForm(FlaskForm):
    currency = SelectField(choices=curr_codes, validators=[DataRequired()])
    startdate = DateField(default=datetime.today, validators=[DataRequired()])
    todate = DateField(default=datetime.today, validators=[DataRequired()])
    submit = SubmitField('Sprawdź')