import json

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, Column, Float

from utils_helpers.AES import decrypt_data

db = SQLAlchemy()


class Transactions(db.Model):
    __tablename__ = 'transactions'

    id = Column(db.Integer, primary_key=True)
    user_id = Column(db.Integer, nullable=False)
    transaction_data = Column(db.String(500), nullable=False)
    creation_time = Column(DateTime, nullable=False)

    def serialize(self):
        decrypted_transaction_data = decrypt_data(str(self.transaction_data))
        data = json.loads(decrypted_transaction_data)
        return {
            "id": self.id,
            "user_id": self.user_id,
            "amount": data["amount"],
            "currency_amount": data["currency_amount"],
            "status": data["status"],
            "creation_time": self.creation_time,
        }
