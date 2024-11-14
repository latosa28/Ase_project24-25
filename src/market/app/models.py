from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Numeric

# Creiamo un'istanza di SQLAlchemy
db = SQLAlchemy()


# Modello per la tabella "market"
class Market(db.Model):
    __tablename__ = 'market'

    market_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # ID univoco per il mercato
    istance_id = db.Column(db.Integer, nullable=False)  # ID dell'istanza dell'asta (non nullo)
    seller_user_id = db.Column(db.Integer, nullable=False)  # ID dell'utente venditore (non nullo)
    buyer_user_id = db.Column(db.Integer, nullable=True)  # ID dell'utente acquirente (può essere nullo)
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # Data e ora di inizio (non nulla)
    end_date = db.Column(db.DateTime, nullable=False)  # Data e ora di fine (non nulla)
    bid = db.Column(Numeric(10, 2), nullable=False, default=0.00)  # L'importo dell'offerta (non nullo)

    def __init__(self, istance_id, seller_user_id, start_date, end_date, bid, buyer_user_id=None):
        self.istance_id = istance_id
        self.seller_user_id = seller_user_id
        self.start_date = start_date
        self.end_date = end_date
        self.bid = bid
        self.buyer_user_id = buyer_user_id

    def serialize(self):
        """Metodo per serializzare l'oggetto in formato JSON."""
        return {
            'market_id': self.market_id,
            'istance_id': self.istance_id,
            'seller_user_id': self.seller_user_id,
            'buyer_user_id': self.buyer_user_id,
            'start_date': self.start_date.isoformat(),  # Formattato come stringa ISO
            'end_date': self.end_date.isoformat(),
            'bid': str(self.bid)  # Converte il valore del bid in stringa per JSON
        }
