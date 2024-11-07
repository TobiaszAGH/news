from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_bootstrap import Bootstrap
from blueprints.main.routes import main_bp
from blueprints.economy.routes import economy_bp
from blueprints.news.routes import news_bp
from blueprints.sport.routes import sport_bp
from blueprints.weather.routes import weather_bp

db = SQLAlchemy()

def create_app():
    # Initialize the app
    app = Flask(__name__)
    Bootstrap(app)
    
    app.config.from_object(Config)

    app.register_blueprint(main_bp, url_prefix='/') 
    app.register_blueprint(economy_bp, url_prefix='/economy')
    app.register_blueprint(news_bp, url_prefix='/news')
    app.register_blueprint(sport_bp, url_prefix='/sport')
    app.register_blueprint(weather_bp, url_prefix='/weather') 

    # Initailize the database
    db.init_app(app)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

