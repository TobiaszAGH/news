from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Config(object):
    SECRET_KEY = 'sridzajarwanapurakotte'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///users.db'