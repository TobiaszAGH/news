from flask import Blueprint, render_template, request
import requests
from blueprints.calendar.scraping import get_proverb, get_agh_news
from datetime import datetime, timedelta

months=['stycznia', 'lutego', 'marca', 'kwietnia', 'maja', 'czerwca', 'lipca', 'sierpnia', 'wrzesnia', 'pazdziernika', 'listopada', 'grudnia']
month_name=['Styczeń', 'Luty', 'Marzec', 'Kwiecień', 'Maj', 'Czerwiec', 'Lipiec', 'Sierpień', 'Wrzesień', 'Październik', 'Listopad', 'Grudzień']

calendar_bp = Blueprint(
    'calendar_bp',
    __name__,
    static_folder='static',
    template_folder='templates'
)

@calendar_bp.route('/calendar_preview')
def calendar_preview():
    date_str = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    date = datetime.strptime(date_str, '%Y-%m-%d')
    
    prev_date = (date - timedelta(days=1)).strftime('%Y-%m-%d')
    next_date = (date + timedelta(days=1)).strftime('%Y-%m-%d')

    nameday_url = f"https://nameday.abalin.net/api/V1/getdate?day={date.day}&month={date.month}&country=pl"
    nameday_response = requests.get(nameday_url)

    holiday_url=f'https://pniedzwiedzinski.github.io/kalendarz-swiat-nietypowych/{date.month}/{date.day}.json'
    holiday_response = requests.get(holiday_url)
    if(date.day<10):
        date2 = f"0{date.day}.{date.month}.{date.year}"
    else: 
        date2 = f"{date.day}.{date.month}.{date.year}"
    agh_news = get_agh_news(date2)

    proverb=get_proverb(date.day, months[date.month-1])
   

    if holiday_response.status_code == 200 and nameday_response.status_code==200:
        nameday_data = nameday_response.json()
        holidays_data = holiday_response.json()
        
        if isinstance(holidays_data, list) and holidays_data:
            holidays = [holiday.get('name', 'Brak nazwy święta') for holiday in holidays_data]
        else:
            holidays = ['Brak świąt']

        nameday = nameday_data.get('nameday', {}).get('pl', '')
        nameday_list = nameday.split(', ') if nameday else ['Brak imienin']

        data = {
            'date': date,
            'month': month_name[date.month-1],
            'nameday': nameday_list,
            'holidays': holidays,
            'proverb': proverb,
            'article': agh_news,
            'prev_date': prev_date,
            'next_date': next_date
        }
        return render_template('calendar.html', **data)
    else:
        return f"Failed to retrieve data with status code {nameday_response.status_code} or {holiday_response.status_code}", 500