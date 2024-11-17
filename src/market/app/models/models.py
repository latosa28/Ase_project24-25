from datetime import datetime
import pytz
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, Numeric


db = SQLAlchemy()


class Market(db.Model):
    __tablename__ = 'market'

    market_id = Column(Integer, primary_key=True, autoincrement=True)  # ID univoco per il mercato
    istance_id = Column(Integer, nullable=False)  # ID dell'istanza dell'asta (non nullo)
    seller_user_id = Column(Integer, nullable=False)  # ID dell'utente venditore (non nullo)
    buyer_user_id = Column(Integer, nullable=True)  # ID dell'utente acquirente (può essere nullo)
    start_date = Column(DateTime, nullable=False, default=datetime.utcnow)  # Data e ora di inizio (non nulla)
    end_date = Column(DateTime, nullable=False)  # Data e ora di fine (non nulla)
    bid = Column(Numeric(10, 2), nullable=False, default=0.00)  # L'importo dell'offerta (non nullo)
    status = Column(String(50), nullable=False)

    def __init__(self, istance_id, seller_user_id, start_date, end_date, bid, status, buyer_user_id=None):
        self.istance_id = istance_id
        self.seller_user_id = seller_user_id
        self.start_date = start_date
        self.end_date = end_date
        self.bid = bid
        self.buyer_user_id = buyer_user_id
        self.status = status

    def serialize(self):
        rome_tz = pytz.timezone('Europe/Rome')
        return {
            'market_id': self.market_id,
            'istance_id': self.istance_id,
            'seller_user_id': self.seller_user_id,
            'buyer_user_id': self.buyer_user_id,
            'start_date': self.start_date.astimezone(rome_tz).isoformat() if self.start_date else None,
            'end_date': self.end_date.astimezone(rome_tz).isoformat() if self.end_date else None,
            'status': self.status,
            'bid': str(self.bid)  # Converte il valore del bid in stringa per JSON
        }
