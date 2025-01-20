"""
Moduł definiuje modele bazy danych dla artykułów kryminalnych oraz powiązanych z nimi obrazów.
"""

from sqlalchemy import ForeignKey
from config import db


class CrimeNews(db.Model):
    """ Model reprezentujący artykuły kryminalne w bazie danych. """

    __tablename__ = 'crime_news'

    id = db.Column(db.Integer, primary_key=True)  # Klucz główny, unikalne id artykułu
    title = db.Column(db.String(255), nullable=False)  # Tytuł artykułu, pole wymagane
    summary = db.Column(db.Text, nullable=False)  # Streszczenie artykułu, pole wymagane
    description = db.Column(db.Text, nullable=True)  # Opis artykułu, pole opcjonalne
    image_url = db.Column(db.String(255), nullable=True)  # URL do obrazu, pole opcjonalne
    article_link = db.Column(db.String(255), nullable=False)  # URL do artykułu, wymagany
    publication_date = db.Column(db.Date, nullable=False)  # Data publikacji, wymagana


class CrimeImage(db.Model):
    """ Model reprezentujący obrazy związane z artykułami kryminalnymi. """
    # Nazwa tabeli w bazie danych
    __tablename__ = 'crime_images'

    id = db.Column(db.Integer, primary_key=True)  # Klucz główny, unikalne id obrazu
    image_url = db.Column(db.String(255), nullable=True)  # URL do obrazu, opcjonalny
    news_id = db.Column(db.Integer, ForeignKey('crime_news.id'), nullable=False)
    # Klucz obcy wskazujący na tabelę 'crime_news', pole wymagane
