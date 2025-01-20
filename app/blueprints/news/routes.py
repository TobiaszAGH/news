"""
Moduł zawierający routes dla modułu news.
"""

from flask import Blueprint, render_template, request
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
    """ Główna strona z artykułami """
    per_page = 5  # Liczba artykułów wyświetlanych na jednej stronie
    page = request.args.get('page', 1, type=int)  # Pobranie numeru strony
    # Paginacja artykułów, sortowanie według daty publikacji (od najnowszych)
    paginated_articles = CrimeNews.query \
        .order_by(desc(CrimeNews.publication_date)) \
        .paginate(page=page, per_page=per_page, error_out=False)

    # Renderowanie szablonu z artykułami
    return render_template('news.html', articles=paginated_articles)


@news_bp.route('/<int:news_id>')
def single_news(news_id):
    """ Pojedynczy artykuł """
    # Pobranie artykułu na podstawie jego ID
    news = db.session.get(CrimeNews, news_id)

    # Jeśli artykuł nie istnieje, wyświetlamy komunikat o błędzie
    if news is None:
        return render_template(
            'single_news.html',
            news=None,
            images=None,
            error="Artykuł o podanym ID nie istnieje lub został usunięty."
        )

    # Pobranie obrazów powiązanych z danym artykułem
    images = CrimeImage.query.filter_by(news_id=news_id).all()

    # Renderowanie szablonu szczegółów artykułu
    return render_template('single_news.html', news=news, images=images)


@news_bp.route('/news_preview')
def news_preview():
    """ Widget wiadomości """
    # Pobranie 5 najnowszych artykułów
    latest_articles = CrimeNews.query \
        .order_by(CrimeNews.publication_date.desc()) \
        .limit(5)

    # Renderowanie szablonu karuzeli dla najnowszych artykułów
    return render_template('news_preview.html', articles=latest_articles)
