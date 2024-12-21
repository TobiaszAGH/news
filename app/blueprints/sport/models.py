from config import db
from datetime import datetime

class SportArticle(db.Model):
    __tablename__ = 'sport_articles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    pubDate = db.Column(db.DateTime, nullable=True)
    link = db.Column(db.String(255), nullable=True)
    sport_type = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<SportArticle {self.title}>'
