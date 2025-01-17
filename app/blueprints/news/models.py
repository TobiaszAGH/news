from sqlalchemy import ForeignKey
from config import db

# Definicja modelu reprezentującego artykuły kryminalne w bazie danych
class CrimeNews(db.Model):
    # Nazwa tabeli w bazie danych
    __tablename__ = 'crime_news'
    # Umożliwia nadpisanie istniejącej tabeli (jeśli jest już zdefiniowana)
    __table_args__ = {'extend_existing': True}

    # Główne pola tabeli
    id = db.Column(db.Integer, primary_key=True)  # Klucz główny, unikalny identyfikator artykułu
    title = db.Column(db.String(255), nullable=False)  # Tytuł artykułu, pole wymagane
    summary = db.Column(db.Text, nullable=False)  # Krótkie streszczenie artykułu, pole wymagane
    description = db.Column(db.Text, nullable=True)  # Szczegółowy opis artykułu, pole opcjonalne
    image_url = db.Column(db.String(255), nullable=True)  # URL do obrazu, pole opcjonalne
    article_link = db.Column(db.String(255), nullable=False)  # URL do pełnego artykułu, pole wymagane
    publication_date = db.Column(db.Date, nullable=False)  # Data publikacji artykułu, pole wymagane

# Definicja modelu reprezentującego obrazy związane z artykułami kryminalnymi
class CrimeImage(db.Model):
    # Nazwa tabeli w bazie danych
    __tablename__ = 'crime_images'
    # Umożliwia nadpisanie istniejącej tabeli (jeśli jest już zdefiniowana)
    __table_args__ = {'extend_existing': True}

    # Główne pola tabeli
    id = db.Column(db.Integer, primary_key=True)  # Klucz główny, unikalny identyfikator obrazu
    image_url = db.Column(db.String(255), nullable=True)  # URL do obrazu, pole opcjonalne
    news_id = db.Column(db.Integer, ForeignKey('crime_news.id'), nullable=False)  
    # Klucz obcy wskazujący na tabelę 'crime_news', pole wymagane
