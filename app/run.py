from app import app, db, scheduler

# Start the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        scheduler.start()
    from blueprints.news.data_scraper import scrape_and_save
    scheduler.add_job(
        id='1',
        func=scrape_and_save,
        trigger='cron',
        hour=00,
        minute=00)
    app.run(debug=False)