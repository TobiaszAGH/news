from flask import Blueprint, render_template, request
import requests
from .models import SportArticle
from config import db
from datetime import datetime

sport_bp = Blueprint(
    'sport',
    __name__,
    static_folder='static',
    template_folder='templates'
)

SPORT_API = {
    "football": "https://newsdata.io/api/1/news?apikey=pub_593496808acfb9d29e8410845a3b9602f5863&q=piłka%20nożna&country=pl&category=sports",
    "tennis": "https://newsdata.io/api/1/news?apikey=pub_593496808acfb9d29e8410845a3b9602f5863&q=tenis&country=pl&category=sports",
    "ski_jumping": "https://newsdata.io/api/1/news?apikey=pub_593496808acfb9d29e8410845a3b9602f5863&q=skoki%20narciarskie&country=pl&category=sports",
    "volleyball": "https://newsdata.io/api/1/news?apikey=pub_593496808acfb9d29e8410845a3b9602f5863&q=siatkówka&country=pl&category=sports"
}

@sport_bp.route('/')
def sport_home():
    sport_names = {
        "football": "Piłka nożna",
        "tennis": "Tenis",
        "ski_jumping": "Skoki narciarskie",
        "volleyball": "Siatkówka"
    }
    selected_discipline = request.args.get('discipline')

    page = request.args.get('page', 1, type=int)
    per_page = 5

    if selected_discipline:
        articles = SportArticle.query.filter_by(sport_type=selected_discipline).order_by(SportArticle.pubDate.desc()).paginate(page=page, per_page=per_page)
    else:
        articles = SportArticle.query.order_by(SportArticle.pubDate.desc()).paginate(page=page, per_page=per_page)
    
    return render_template('sport.html', articles=articles, sport_names=sport_names)

def fetch_and_save_articles():
    from app import app
    with app.app_context():
        for sport_type, api_url in SPORT_API.items():
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                for article in data.get("results", []):
                    existing_article = SportArticle.query.filter_by(title=article.get("title")).first()
                    if not existing_article:
                        pub_date_str = article.get("pubDate")
                        pub_date = datetime.strptime(pub_date_str, "%Y-%m-%d %H:%M:%S") if pub_date_str else None
                        
                        new_article = SportArticle(
                            title=article.get("title"),
                            description=article.get("description"),
                            image_url=article.get("image_url"),
                            pubDate=pub_date,
                            link=article.get("link"),
                            sport_type=sport_type
                        )
                        db.session.add(new_article)
                db.session.commit()
            

@sport_bp.route('/sport_preview')
def sport_preview():
    disciplines = ['football', 'tennis', 'ski_jumping', 'volleyball']
    articles = []
    
    for discipline in disciplines:
        article = SportArticle.query.filter_by(sport_type=discipline).order_by(SportArticle.pubDate.desc()).first()
        if article:
            articles.append(article)

    sport_names = {
        'football': 'Piłka Nożna',
        'tennis': 'Tenis',
        'ski_jumping': 'Skoki Narciarskie',
        'volleyball': 'Siatkówka',
    }

    return render_template('sport_preview.html', articles=articles, sport_names=sport_names)
