from flask import Blueprint, render_template, request
from blueprints.calendar.functions import get_proverb, get_agh_news, parse_date, get_nameday, get_holiday
from datetime import datetime

# Miesiące w języku polskim
months = [
    'stycznia', 'lutego', 'marca', 'kwietnia', 'maja', 'czerwca',
    'lipca', 'sierpnia', 'września', 'października', 'listopada', 'grudnia'
]
month_name = [
    'Styczeń', 'Luty', 'Marzec', 'Kwiecień', 'Maj', 'Czerwiec',
    'Lipiec', 'Sierpień', 'Wrzesień', 'Październik', 'Listopad', 'Grudzień'
]

# Definicja blueprintu
calendar_bp = Blueprint(
    'calendar_bp',
    __name__,
    static_folder='static',
    template_folder='templates'
)


@calendar_bp.route('/calendar_preview')
def calendar_preview():
    date_str = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    date, prev_date, next_date = parse_date(date_str)

    agh_news = get_agh_news(date)
    proverb = get_proverb(date.day, months[date.month - 1])
    nameday_list = get_nameday(date)
    holidays = get_holiday(date)

    data = {
        'date': date,
        'month': month_name[date.month - 1],
        'nameday': nameday_list,
        'holidays': holidays,
        'proverb': proverb,
        'article': agh_news,
        'prev_date': prev_date,
        'next_date': next_date,
    }
    return render_template('calendar.html', **data)
