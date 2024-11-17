import requests
from models import *
import time
# from datetime import datetime
from bs4 import BeautifulSoup
from app import db

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
            summary = article.find('p').get_text(strip=True)
            image = article.find('img')['src']
            image_src = base_url + image
            date = article.find('span', class_='data').get_text(strip=True).replace("Dodano: ", "").strip()
            full_link = base_url + link
            
            # Treść artykułu, zdjęcia
            response2 = requests.get(full_link)
            soup2 = BeautifulSoup(response2.text, 'html.parser')
            paragraphs = soup2.find_all('p')
            intro = paragraphs[2].get_text(strip=True)
            description = paragraphs[3].get_text(strip=True)
            full_text = intro + '\n' + description
            
            images = soup2.find_all('img')
            image_urls = []
            for img in images:
                img_url = img.get('src')
                img_url = base_url + img_url
                image_urls.append(img_url)
            
            
            # Tworzenie obiektu artykułu
            news_obj = CrimeNews(
                title=title,
                summary=summary,
                full_text=full_text,
                timestamp=date,
                article_link=full_link,
                image_url=image_src
            )
            
            # query="INSERT INTO crime_news VALUE {%s}"
            val={}
            # Tworzenie obiektów zdjęć dla danego artykułu
         
            
            time.sleep(5)
            
else:
    print("Nie udało się pobrać strony:", response.status_code)
    