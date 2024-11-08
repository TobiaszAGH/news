from app import create_app, db, config


# Start the app
if __name__ == '__main__':
    app = create_app(config.Config)
    with app.app_context():
        db.create_all()
    app.run(debug=False)