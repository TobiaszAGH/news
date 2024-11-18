from sqlalchemy import ForeignKey
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app import db

class CrimeNews(db.Model):
    __tablename__ = 'crime_news'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    summary = db.Column(db.Text, nullable=False)
    full_text = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    article_link = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

class CrimeImages(db.Model):
    __tablename__ = 'crime_images'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(255), nullable=True)
    news_id = db.Column(db.Integer, ForeignKey('crime_news.id'), nullable=False)