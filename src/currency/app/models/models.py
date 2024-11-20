from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Currency(db.Model):
    __tablename__ = 'currency'
    user_id = db.Column(db.String(50), primary_key=True)
    amount = db.Column(db.Float, nullable=False, default=0.0)

    def __init__(self, user_id, amount=0.0):
        self.user_id = user_id
        self.amount = amount
