import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


# scrapowanie przysłów
def get_proverb(day, month):
    response = requests.get(f"https://www.kalbi.pl/{day}-{month}")
    soup = BeautifulSoup(response.content, 'html.parser')
    # znalezienie sekcji z przysłowiami
    proverb_text = soup.find(class_='calCard_proverb-content').text.strip()
    proverbs = [p.strip() for p in proverb_text.split('„') if p]
    proverbs = [p.rstrip('”') for p in proverbs]
    return proverbs


# scrapowanie aktualności ze strony agh
def get_agh_news(date):
    base_url = "https://www.agh.edu.pl"
    response = requests.get("https://www.agh.edu.pl/aktualnosci")
    soup = BeautifulSoup(response.content, 'html.parser')
    # znalezienie artykułu
    articles = soup.find_all('article', class_='d-md-flex')

    date2 = f"{date.day:02d}.{date.month:02d}.{date.year}"

    for article in articles:
        # pobranie daty publikacji artykułu
        date_element = article.find('span', class_='date')
        link_element = article.find_parent('a')

        if date_element and date_element.text.strip() == date2:
            title = article.find('h2').text.strip()
            description = article.find('p').text.strip()

            # zbudowanie pełnego linku do artykułu
            if link_element and 'href' in link_element.attrs:
                href = link_element['href']
                link = f"{base_url}{href}" if href.startswith('/aktualnosci') else None
            else:
                link = None

            return {
                'title': title,
                'description': description,
                'link': link,
            }

    return None


def parse_date(date_str):
    date = datetime.strptime(date_str, '%Y-%m-%d')
    prev_date = (date - timedelta(days=1)).strftime('%Y-%m-%d')
    next_date = (date + timedelta(days=1)).strftime('%Y-%m-%d')
    return date, prev_date, next_date


# pobieranie imienin z API
def get_nameday(date):
    nameday_url = f"https://nameday.abalin.net/api/V1/getdate?day={date.day}&month={date.month}&country=pl"
    nameday_response = requests.get(nameday_url)

    if nameday_response.status_code == 200:
        nameday_data = nameday_response.json()
        nameday = nameday_data.get('nameday', {}).get('pl', '')
        return nameday.split(', ') if nameday else ['Brak imienin']

    return ['Brak imienin'], 500


# pobieranie świąt z API
def get_holiday(date):
    holiday_url = f"https://pniedzwiedzinski.github.io/kalendarz-swiat-nietypowych/{date.month}/{date.day}.json"
    holiday_response = requests.get(holiday_url)

    if holiday_response.status_code == 200:
        holidays_data = holiday_response.json()

        if isinstance(holidays_data, list) and holidays_data:
            return [holiday.get('name', 'Brak nazwy święta') for holiday in holidays_data]

        return ['Brak nazwy święta']

    return ['Brak nazwy święta'], 500
