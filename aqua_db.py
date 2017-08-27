from flask_sqlalchemy import SQLAlchemy

def setup(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///aqua.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)
    db.create_all()
    return db

class AquaDB():
    def __init__(self, app):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///aqua.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db = SQLAlchemy(app)
        db.create_all()
        self.db = db
        return self
