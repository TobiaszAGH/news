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

