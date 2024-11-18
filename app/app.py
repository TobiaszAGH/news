from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from blueprints.main.routes import main_bp
from blueprints.economy.routes import economy_bp

from blueprints.sport.routes import sport_bp
from blueprints.weather.routes import weather_bp

db = SQLAlchemy()

# routes wykorzystuje models.py, które pobiera db z app, więc przeniosłam to tu na razie tak prowizorycznie żeby uniknąć błędów importu
from blueprints.news.routes import news_bp

# Initialize the app
app = Flask(__name__)
Bootstrap(app)

from config import Config
app.config.from_object(Config)

app.register_blueprint(main_bp, url_prefix='/') 
app.register_blueprint(economy_bp, url_prefix='/economy')
app.register_blueprint(news_bp, url_prefix='/news')
app.register_blueprint(sport_bp, url_prefix='/sport')
app.register_blueprint(weather_bp, url_prefix='/weather') 

# Initailize the database
db.init_app(app)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

