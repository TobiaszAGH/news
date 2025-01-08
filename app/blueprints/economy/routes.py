from flask import Blueprint, render_template, request, flash
from .forms import EconomyForm
from datetime import timedelta
from data_visualization import generate_graph_html
from .economyData import economyData
from .functions import get_current_codes_and_last_date

economy_bp = Blueprint(
    'economy_bp',
    __name__,
    static_folder='static',
    template_folder='templates'
)

@economy_bp.route('/', methods=['GET','POST'])
def index():
    available_curr_codes, last_date = get_current_codes_and_last_date()
    form = EconomyForm()
    form.currency1.choices = available_curr_codes
    form.currency2.choices = available_curr_codes
    form.currency3.choices = available_curr_codes
    
    
    if request.method == 'GET':
        form.currency1.default = 'Wybierz walutę'
        form.currency2.default = 'Wybierz walutę'
        form.currency3.default = 'Wybierz walutę'
        form.startdate.default = last_date - timedelta(days=7)
        form.todate.default = last_date
        form.process()

        economy_data = economyData()
        economy_data.default()
        graph = economy_data.graph()
        return render_template('economy.html', form=form, graph=graph, page='economy_bp.index')
    
    # load data from form
    curr_codes = [form.currency1.data, form.currency2.data, form.currency3.data]
    startdate = form.startdate.data
    todate = form.todate.data
    economy_data = economyData()
    economy_data.load(curr_codes, startdate, todate, last_date)
    economy_data.fetch_api()
    graph=economy_data.graph()

    return render_template('economy.html', form=form, graph=graph, page='economy_bp.index')
    

@economy_bp.route('/preview')
def preview():
    economy_data = economyData()
    economy_data.default()
    return'<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>' + economy_data.graph(leg=False)