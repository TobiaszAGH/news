from flask import Blueprint, render_template
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import time
# from .data_scraper import data_scrape

news_bp = Blueprint(
    'news_bp',
    __name__,
    static_folder='static',
    template_folder='templates'
)

base_url = "https://krakow.policja.gov.pl"
url = "https://krakow.policja.gov.pl/kr1/aktualnosci"
response = requests.get(url)


@news_bp.route('/')
def index():
    articles_data = []  # Lista do przechowywania artykułów
    # images_data = []

    if response.status_code == 200:
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            articles = soup.find_all('li', class_='news')

            for article in articles:
                
                link = article.find('a')['href']
                
                if link.startswith("/"):
                    # Nagłówek, streszczenie, data publikacji, link do artykułu, zdjęcie
                    title = article.find('strong').get_text(strip=True)
                    
                    """ existing_news = articles_data.filter_by(title=title).first()
                    if existing_news:
                        print(f"Article '{title}' had been already saved.")
                        continue """
                    
                    summary = article.find('p').get_text(strip=True)
                    image = article.find('img')['src']
                    image_src = base_url + image
                    date = article.find('span', class_='data').get_text(strip=True).replace("Dodano: ", "").strip()
                    full_link = base_url + link
                    
                    timestamp = datetime.strptime(date, "%d.%m.%Y")
                    
                    # Treść artykułu, zdjęcia
                    response2 = requests.get(full_link)
                    soup2 = BeautifulSoup(response2.text, 'html.parser')
                    paragraphs = soup2.find_all('p')
                    description = paragraphs[3].get_text(strip=True)
                    full_text = summary + '\n' + description
                    
                                
                    # Tworzenie obiektu artykułu
                    articles_data.append({
                        "title": title,
                        "summary": summary,
                        "full_text":full_text,
                        "image_url":image_src,
                        "article_link": full_link,
                        "timestamp":timestamp
                    })
                    
                    """  images = soup2.find_all('img')
                    for img in images:
                        img_url = img.get('src')
                        img_url = base_url + img_url
                        
                        images_data.append(
                            image_url=img_url,
                            news_id=articles_data.id
                        )    """    
                    # time.sleep(5)
                    
    else:
            print("Connection failed.", response.status_code)
    return render_template('news.html', articles=articles_data)
