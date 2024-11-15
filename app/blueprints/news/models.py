from app import db

class CrimeNews(db.Model):
    __tablename__ = 'crime_news'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    summary = db.Column(db.Text, nullable=False)
    full_text = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    article_link = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    
    images = db.relationship('CrimeImages', back_populates='crime_news')


class CrimeImages(db.Model):
    __tablename__ = 'crime_images'
    
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(255), nullable=True)
    news_id = db.Column(db.Integer, db.ForeignKey('crime_news.id'), nullable=False)
    
    news = db.relationship('CrimeNews', back_populates='crime_images')
    