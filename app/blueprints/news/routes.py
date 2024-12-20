from flask import Blueprint, render_template, request, abort
from sqlalchemy import desc
from config import db
from .models import CrimeNews, CrimeImage

news_bp = Blueprint(
    'news_bp',
    __name__,
    static_folder='static',
    template_folder='templates'
)

@news_bp.route('/')
def news_home():
    per_page = 5
    page = request.args.get('page', 1, type=int)
    paginated_articles = CrimeNews.query \
    .order_by(desc(CrimeNews.publication_date)) \
    .paginate(page=page, per_page=per_page, error_out=False)

    return render_template('news.html', articles=paginated_articles)


@news_bp.route('/<int:news_id>')
def single_news(news_id):
    news = db.session.get(CrimeNews, news_id)

    if news is None:
        abort(404)

    images = CrimeImage.query.filter_by(news_id=news_id).all()

    return render_template('single_news.html', news=news, images=images)


@news_bp.route('/news_preview')
def news_preview():
    latest_articles = CrimeNews.query.order_by(CrimeNews.publication_date.desc()).limit(5)

    return render_template('news_preview.html', articles=latest_articles)
