from flask import Flask

from flask_bootstrap import Bootstrap
from flask_apscheduler import APScheduler
from blueprints.main.routes import main_bp
from blueprints.economy.routes import economy_bp
from blueprints.sport.routes import sport_bp
from blueprints.weather.routes import weather_bp
from blueprints.calendar.routes import calendar_bp


scheduler=APScheduler()

# Initialize the app
app = Flask(__name__)
Bootstrap(app)

from blueprints.news.routes import news_bp

from config import Config, db
app.config.from_object(Config)


app.register_blueprint(main_bp, url_prefix='/') 
app.register_blueprint(economy_bp, url_prefix='/economy')
app.register_blueprint(news_bp, url_prefix='/news')
app.register_blueprint(sport_bp, url_prefix='/sport')
app.register_blueprint(weather_bp, url_prefix='/weather') 
app.register_blueprint(calendar_bp, url_prefix='/calendar')

# Initailize the database
db.init_app(app)
scheduler.init_app(app)




if __name__ == '__main__':
    with app.app_context():
        scheduler.start()
        db.create_all()
    from blueprints.news.data_scraper import scrape_and_save
    scheduler.add_job(
        id='1',
        func=scrape_and_save,
        trigger='cron',
        hour=0,
        minute=0)
    from blueprints.sport.routes import fetch_and_save_articles
    scheduler.add_job(
        id='fetch_sport_articles',
        func=fetch_and_save_articles,
        trigger='cron',
        hour=0,
        minute=0)
    app.run(debug=True, port=8000)

