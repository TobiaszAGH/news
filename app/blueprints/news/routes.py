from flask import Blueprint, render_template
from .models import CrimeNews
from .data_scraper import data_scrape

news_bp = Blueprint(
    'news_bp',
    __name__,
    static_folder='static',
    template_folder='templates'
)

@news_bp.route('/')
def news_home():
    articles_data=CrimeNews.query.all()
    return render_template('news.html', articles=articles_data)

