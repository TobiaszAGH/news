from flask import Blueprint, render_template, request
from .forms import EconomyForm
import requests
from datetime import timedelta

economy_bp = Blueprint(
    'economy_bp',
    __name__,
    static_folder='static',
    template_folder='templates'
)


@economy_bp.route('/', methods=['GET','POST'])
def index():
    form = EconomyForm()
    if request.method == 'GET':
        return render_template('economy.html', form=form)
    
    curr_code = form.currency.data
    startdate = form.startdate.data
    todate = form.todate.data
    if startdate > todate:
        return 'Start musi być wcześniej niż koniec'
    if todate - startdate > timedelta(days=93):
        return 'Zakres nie może przekraczać 93 dni'
    link = f'https://api.nbp.pl/api/exchangerates/rates/A/{curr_code}/{startdate}/{todate}'
    data = requests.get(link).json()
    return data
