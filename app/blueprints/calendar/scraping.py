import requests
from bs4 import BeautifulSoup

def get_proverb(day, month):
    response = requests.get(f"https://www.kalbi.pl/{day}-{month}")
    soup = BeautifulSoup(response.content,'html.parser')
    proverb_text= soup.find(class_='calCard_proverb-content').text.strip()
    proverbs = [p.strip() for p in proverb_text.split('„') if p]
    proverbs = [p.rstrip('”') for p in proverbs]
    return proverbs

def get_agh_news(date):
    base_url = "https://www.agh.edu.pl"
    response=requests.get(f"https://www.agh.edu.pl/aktualnosci")
    soup=BeautifulSoup(response.content, 'html.parser')
    articles=soup.find_all('article', class_='d-md-flex')
    for article in articles:
        date_element = article.find('span', class_='date')
        if date_element and date_element.text.strip() == date:
            title = article.find('h2').text.strip()  
            description = article.find('p').text.strip() 
            link_element = article.find_parent('a')
            if link_element and 'href' in link_element.attrs:
                link = f"{base_url}{link_element['href']}"  
            else:
                link = None


            return {
                'title': title,
                'description': description,
                'link': link
            }

    return None