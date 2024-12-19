import time
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from app import app
from config import db
from .models import CrimeNews, CrimeImage

base_url = "https://krakow.policja.gov.pl"
url = "https://krakow.policja.gov.pl/kr1/aktualnosci"
response = requests.get(url)

def fetch_article(article, title):
    summary = article.find('p').get_text(strip=True)
    image_src = base_url + article.find('img')['src']
    date_str = article.find('span', class_='data') \
        .get_text(strip=True).replace("Dodano: ", "").strip()
    date = datetime.strptime(date_str, "%d.%m.%Y").date()
    return {'title': title, 'summary': summary, 'image_src': image_src, 'date': date}

def fetch_article_description(full_link):
    response2 = requests.get(full_link)
    soup2 = BeautifulSoup(response2.text, 'html.parser')
    paragraphs = soup2.find_all('p')
    description = paragraphs[3].get_text(strip=True)
    return description, soup2

def save_article(article_data, full_link, description):
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
        db.session.commit()
        print(f"Article: '{article_data['title']}' saved to database.")
    except Exception as e:
        db.session.rollback()
        print(f"Error during saving article: '{article_data['title']}' to database: {e}")
    return news_obj

def save_images(soup2, news_obj):
    images = soup2.find_all('img')
    for img in images:
        img_url = img.get('src')
        img_url = base_url + img_url
        img_obj = CrimeImage(
            image_url=img_url,
            news_id=news_obj.id
        )
        db.session.add(img_obj)
    try:
        db.session.commit()
        print(f"Images from news: '{news_obj.title}' saved to database.")
    except Exception as e:
        db.session.rollback()
        print(f"Error during saving images for news: '{news_obj.title}' to database: {e}")

def scrape_and_save():
    with app.app_context():
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            articles = soup.find_all('li', class_='news')

            for article in articles:
                link = article.find('a')['href']

                if link.startswith("/"):
                    title = article.find('strong').get_text(strip=True)

                    if CrimeNews.query.filter_by(title=title).first():
                        print(f"Article '{title}' has already been saved.")
                        print("No new articles to process.")
                        return

                    article_data = fetch_article(article, title)

                    full_link = base_url + link
                    description, soup2 = fetch_article_description(full_link)

                    news_obj = save_article(article_data, full_link, description)
                    save_images(soup2, news_obj)

                    time.sleep(2)
        
        else:
            print("Connection failed.", response.status_code)
