from flask import Blueprint, render_template
from .models import CrimeNews
from sqlalchemy import desc

news_bp = Blueprint(
    'news_bp',
    __name__,
    static_folder='static',
    template_folder='templates'
)

@news_bp.route('/')
def news_home():
    articles_data=CrimeNews.query.order_by(desc(CrimeNews.publication_date)).all()
    return render_template('news.html', articles=articles_data)


@news_bp.route('/<int:news_id>')
def single_news(news_id):
    
    news = CrimeNews.query.get(news_id)
    
    images = CrimeImage.query.filter_by(news_id=news_id).all()

    return render_template('single_news.html', news=news, images=images)


@news_bp.route('/news_preview')
def news_preview():
    latest_articles = CrimeNews.query.order_by(CrimeNews.timestamp.desc()).limit(5).all()
    return render_template('news_preview.html', latest_articles=latest_articles)
