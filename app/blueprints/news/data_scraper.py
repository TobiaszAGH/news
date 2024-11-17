import requests
from models import CrimeNews, CrimeImages
from datetime import datetime
from bs4 import BeautifulSoup
from app import db
import time

base_url = "https://krakow.policja.gov.pl"
url = "https://krakow.policja.gov.pl/kr1/aktualnosci"

response = requests.get(url)

if response.status_code == 200:
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    articles = soup.find_all('li', class_='news')

    for article in articles:
        
        link = article.find('a')['href']
        
        if link.startswith("/"):
            # Nagłówek, streszczenie, data publikacji, link do artykułu, zdjęcie
            title = article.find('strong').get_text(strip=True)
            
            existing_news = CrimeNews.query.filter_by(title=title).first()
            if existing_news:
                print(f"Artykuł '{title}' już istnieje w bazie danych.")
                continue
            
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
            intro = paragraphs[2].get_text(strip=True)
            description = paragraphs[3].get_text(strip=True)
            full_text = intro + '\n' + description
            
            
            
            # Tworzenie obiektu artykułu
            news_obj = CrimeNews(
                title=title,
                summary=summary,
                full_text=full_text,
                timestamp=timestamp,
                article_link=full_link,
                image_url=image_src
            )
            db.session.add(news_obj)
            
            images = soup2.find_all('img')
            image_urls = []
            for img in images:
                img_url = img.get('src')
                img_url = base_url + img_url
                image_urls.append(img_url)
                
                img_obj= CrimeImages(
                    image_url=img_url,
                    news=news_obj
                )
                db.session.add(img_obj)
        
            # Zapis do bazy danych
            try:
                db.session.commit()  # Zatwierdzanie zmian w bazie
                print(f"Artykuł '{title}' został zapisany.")
            except Exception as e:
                db.session.rollback()  # Cofanie zmian w przypadku błędu
                print(f"Error during saving data to database '{title}': {e}")

            
            time.sleep(5)
            
else:
    print("Connection failed.", response.status_code)
    