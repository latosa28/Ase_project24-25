
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, Column, Float

db = SQLAlchemy()


class Transactions(db.Model):
    __tablename__ = 'transactions'

    id = Column(db.Integer, primary_key=True)
    user_id = Column(db.Integer, nullable=False)
    card_number = Column(db.String(16), nullable=False)
    card_expiry = Column(db.String(5), nullable=False)
    card_cvc = Column(db.String(3), nullable=False)
    amount = Column(db.Float, nullable=False)  # Importo pagato in EUR
    currency_amount = Column(
        Float, nullable=False
    )  # Quantità di currency speciale acquistata
    status = Column(db.String(20), nullable=False)
    created_at = Column(DateTime, nullable=False)

    def __repr__(self):
        return f"<Transaction {self.id} - {self.status}>"

    def serialize(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "currency_amount": self.currency_amount,
            "status": self.status,
            "created_at": self.created_at,
        }
