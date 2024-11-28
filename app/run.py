from app import app, db, scheduler

# Start the app
if __name__ == '__main__':
    with app.app_context():
        scheduler.start()
        db.create_all()
    app.run(debug=False)