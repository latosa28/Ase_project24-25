# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Item(db.Model):
    __tablename__ = 'item'

    item_id = db.Column(db.Integer, primary_key=True)
    rarity = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False, unique=True)
    image_path = db.Column(db.String(255), nullable=False)

    def __init__(self, rarity, name, image_path):
        self.rarity = rarity
        self.name = name
        self.image_path = image_path


class UserItem(db.Model):
    __tablename__ = 'user_item'

    istance_id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.item_id'), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    date_roll = db.Column(db.DateTime, nullable=False)

    item = db.relationship('Item', backref=db.backref('user_items', lazy=True))

    def __init__(self, item_id, user_id, date_roll):
        self.item_id = item_id
        self.user_id = user_id
        self.date_roll = date_roll
