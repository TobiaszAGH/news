from app import app, db, scheduler
from blueprints.news.data_scraper import scrape_and_save

# Start the app
def main():
    with app.app_context():
        db.create_all()
        scheduler.start()
    scrape_and_save()
    scheduler.add_job(
        id='1',
        func=scrape_and_save,
        trigger='cron',
        hour=0,
        minute=0)
    return app
