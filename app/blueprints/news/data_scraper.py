"""
Moduł do scrapowania wiadomości ze strony krakowskiej policji.
"""

import time
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from sqlalchemy.exc import SQLAlchemyError
from config import db
from app import app
from .models import CrimeNews, CrimeImage

# Adres bazowy strony policji w Krakowie
BASE_URL = "https://krakow.policja.gov.pl"

# Adres URL strony z aktualnościami
URL = "https://krakow.policja.gov.pl/kr1/aktualnosci"

response = requests.get(URL, timeout=10)


def fetch_article(article, title):
    """ Pobiera dane artykułu: tytuł, podsumowanie, obrazek, data. """
    summary = article.find('p').get_text(strip=True)
    image_src = BASE_URL + article.find('img')['src']

    # Pobranie i sformatowanie daty publikacji artykułu
    date_str = article.find('span', class_='data') \
        .get_text(strip=True).replace("Dodano: ", "").strip()
    date = datetime.strptime(date_str, "%d.%m.%Y").date()

    # Zwrócenie danych artykułu w postaci słownika
    return {'title': title, 'summary': summary, 'image_src': image_src, 'date': date}


def fetch_article_description(full_link):
    """ Pobiera pełny opis artykułu. """
    # Pobranie pełnego opisu artykułu z podanej strony
    response2 = requests.get(full_link, timeout=10)
    soup2 = BeautifulSoup(response2.text, 'html.parser')
    paragraphs = soup2.find_all('p')

    # Pobranie czwartego paragrafu jako szczegółowego opisu
    description = paragraphs[3].get_text(strip=True)
    return description, soup2


def save_article(article_data, full_link, description):
    """ Zapisuje artykuł do bazy danych. """

    # Tworzenie obiektu artykułu z pobranych danych
    news_obj = CrimeNews(
        title=article_data['title'],
        summary=article_data['summary'],
        description=description,
        image_url=article_data['image_src'],
        article_link=full_link,
        publication_date=article_data['date']
    )
    db.session.add(news_obj)
    try:
        # Próba zapisania artykułu do bazy danych
        db.session.commit()
        print(f"Artykuł: '{article_data['title']}' zapisany do bazy danych.")
    except SQLAlchemyError as e:
        # Wycofanie transakcji w przypadku błędu
        db.session.rollback()
        print(f"Błąd podczas zapisywania artykułu: '{article_data['title']}' do bazy danych: {e}")
    return news_obj


def save_images(soup2, news_obj):
    """ Zapisuje obrazy z artykułu do bazy danych."""
    # Pobranie wszystkich obrazów z artykułu
    images = soup2.find_all('img')
    for img in images:
        img_url = img.get('src')
        img_url = BASE_URL + img_url
        # Tworzenie obiektu obrazu dla każdego znalezionego obrazu
        img_obj = CrimeImage(
            image_url=img_url,
            news_id=news_obj.id
        )
        db.session.add(img_obj)
    try:
        # Próba zapisania obrazów do bazy danych
        db.session.commit()
        print(f"Obrazy z artykułu: '{news_obj.title}' zostały zapisane do bazy danych.")
    except SQLAlchemyError as e:
        # Wycofanie transakcji w przypadku błędu
        db.session.rollback()
        print(f"Błąd podczas zapisywania obrazów dla artykułu: '{news_obj.title}' do bazy: {e}")


def scrape_and_save():
    """ Główna funkcja odpowiedzialna za scrapowanie i zapisywanie artykułów."""
    # Użycie kontekstu aplikacji do obsługi bazy danych
    with app.app_context():
        if response.status_code == 200:
            # Jeśli połączenie z URL powiodło się
            soup = BeautifulSoup(response.text, 'html.parser')
            articles = soup.find_all('li', class_='news')

            for article in articles:
                # Pobranie linku do pełnego artykułu
                link = article.find('a')['href']

                if link.startswith("/"):
                    # Pobranie tytułu artykułu
                    title = article.find('strong').get_text(strip=True)

                    # Sprawdzenie, czy artykuł już istnieje w bazie danych
                    if CrimeNews.query.filter_by(title=title).first():
                        print(f"Artykuł: '{title}' znajduje się już w bazie danych.")
                        print("Brak nowych artykułów do zapisu.")
                        return

                    # Pobranie danych artykułu
                    article_data = fetch_article(article, title)

                    # Pełny link do artykułu
                    full_link = BASE_URL + link
                    # Pobranie szczegółowego opisu artykułu
                    description, soup2 = fetch_article_description(full_link)

                    # Zapisanie artykułu do bazy danych
                    news_obj = save_article(article_data, full_link, description)

                    # Zapisanie obrazów z artykułu
                    save_images(soup2, news_obj)

                    # Opóźnienie między kolejnymi żądaniami
                    time.sleep(2)

        else:
            # Jeśli połączenie z URL nie powiodło się
            print("Nie udało się połączyć z serwisem policja.pl.", response.status_code)
