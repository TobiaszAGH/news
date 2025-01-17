from flask_wtf import FlaskForm
from wtforms import DateField, SubmitField, SelectField


class EconomyForm(FlaskForm):
    currency1 = SelectField()
    currency2 = SelectField()
    currency3 = SelectField()
    startdate = DateField(label='Od')
    todate = DateField(label='Do')
    submit = SubmitField('Sprawdź')
