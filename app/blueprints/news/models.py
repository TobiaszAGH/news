from sqlalchemy import ForeignKey
from config import db

class CrimeNews(db.Model):
    __tablename__ = 'crime_news'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    summary = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    article_link = db.Column(db.String(255), nullable=False)
    publication_date = db.Column(db.Date, nullable=False)

class CrimeImage(db.Model):
    __tablename__ = 'crime_images'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(255), nullable=True)
    news_id = db.Column(db.Integer, ForeignKey('crime_news.id'), nullable=False)
    