import requests
from .models import CrimeNews, CrimeImage
from datetime import datetime
from bs4 import BeautifulSoup
import time
from config import db
from app_setup import app

base_url = "https://krakow.policja.gov.pl"
url = "https://krakow.policja.gov.pl/kr1/aktualnosci"

response = requests.get(url)

def scrape_and_save():
    with app.app_context(): 
        if response.status_code == 200:

            soup = BeautifulSoup(response.text, 'html.parser')
            articles = soup.find_all('li', class_='news')

            for article in articles:
                
                link = article.find('a')['href']
                
                if link.startswith("/"):
                    
                    title = article.find('strong').get_text(strip=True)
                    
                    # zakładam, że tytuł artykułu nie będzie zmieniany, inaczej artykuł zostanie zduplikowany w bazie
                    existing_news = CrimeNews.query.filter_by(title=title).first()
                    if existing_news:
                        print(f"Article '{title}' had been already saved.")
                        print("No new articles to process.")
                        return
                    
                    summary = article.find('p').get_text(strip=True)
                    
                    image = article.find('img')['src']
                    image_src = base_url + image
                    
                    date = article.find('span', class_='data').get_text(strip=True).replace("Dodano: ", "").strip()
                    
                    full_link = base_url + link
                    
                    publication_date = datetime.strptime(date, "%d.%m.%Y").date()
                    
                    
                    response2 = requests.get(full_link)
                    soup2 = BeautifulSoup(response2.text, 'html.parser')
                    paragraphs = soup2.find_all('p')
                    description = paragraphs[3].get_text(strip=True)
                    full_text = summary + '\n' + description
                    
                        
                    news_obj = CrimeNews(
                        title=title,
                        summary=summary,
                        full_text=full_text,
                        image_url=image_src,
                        article_link=full_link,
                        publication_date=publication_date
                    )
                    db.session.add(news_obj)
                    try:
                        db.session.commit()
                        print(f"Article: '{title}' saved to database.")
                    except Exception as e:
                        db.session.rollback()
                        print(f"Error during saving article: '{title}' to database: {e}")

                    
                    
                    images = soup2.find_all('img')
                    for img in images:
                        img_url = img.get('src')
                        img_url = base_url + img_url
                        
                        img_obj= CrimeImage(
                            image_url=img_url,
                            news_id=news_obj.id
                        )
                        db.session.add(img_obj)         
                    
                    
                    try:
                        db.session.commit()
                        print(f"Images from news: '{title}' saved to database.")
                    except Exception as e:
                        db.session.rollback()
                        print(f"Error during saving images for news: '{title}' to database: {e}")

                    time.sleep(2) 
                    
        else:
            print("Connection failed.", response.status_code)
