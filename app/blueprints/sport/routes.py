from flask import Blueprint, render_template, request
import requests

sport_bp = Blueprint('sport', __name__, template_folder='templates')

SPORT_API = {
    "football": "https://newsdata.io/api/1/news?apikey=pub_593496808acfb9d29e8410845a3b9602f5863&q=piłka%20nożna&country=pl&category=sports",
    "tennis": "https://newsdata.io/api/1/news?apikey=pub_593496808acfb9d29e8410845a3b9602f5863&q=tenis&country=pl&category=sports",
    "ski_jumping": "https://newsdata.io/api/1/news?apikey=pub_593496808acfb9d29e8410845a3b9602f5863&q=skoki%20narciarskie&country=pl&category=sports",
    "volleyball": "https://newsdata.io/api/1/news?apikey=pub_593496808acfb9d29e8410845a3b9602f5863&q=siatkówka&country=pl&category=sports"
}

@sport_bp.route('/')
def sport_home():
    return render_template('sport.html')

@sport_bp.route('/articles/<sport_type>')
def sport_articles(sport_type):
    api_url = SPORT_API.get(sport_type)
    sport_names = {
        "football": "Piłka Nożna",
        "tennis": "Tenis",
        "ski_jumping": "Skoki Narciarskie",
        "volleyball": "Siatkówka"
    }
    sport_name = sport_names.get(sport_type, "Nieznany Sport")
    
    if not api_url:
        return render_template('articles.html', articles=[], sport_name=sport_name, error="Nieznany sport!")

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        articles = [
            {
                "title": article.get("title"),
                "description": article.get("description"),
                "image": article.get("image_url"),
                "link": article.get("link"),
                "pubDate": article.get("pubDate")
            }
            for article in data.get("results", [])
        ]
        return render_template('articles.html', articles=articles, sport_name=sport_name)
    except Exception as e:
        return render_template('articles.html', articles=[], sport_name=sport_name, error="Nie udało się pobrać artykułów!")
