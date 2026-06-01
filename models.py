# models.py
from extensions import db

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    igdb_id = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Float)
    release_date = db.Column(db.String(20)) 
    cover_url = db.Column(db.String(255))

    def __repr__(self):
        return f"<Game {self.name}>"