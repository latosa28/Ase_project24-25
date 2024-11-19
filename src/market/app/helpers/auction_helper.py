import logging
from datetime import datetime
from helpers.collection import CollectionHelper
from helpers.currency import CurrencyHelper
from models.models import Market, db


def handle_expired_auction(auction):
    try:
        logging.info(f"Auction {auction.market_id} has expired, processing...")
        auction.status = "expired"
        if auction.buyer_user_id:
            CurrencyHelper().add_amount(auction.seller_user_id, auction.bid)
            CollectionHelper().move_instance(
                auction.seller_user_id, auction.buyer_user_id, auction.istance_id
            )
        db.session.commit()
        logging.info(f"Auction {auction.market_id} closed successfully.")
    except Exception as e:
        logging.error(f"Auction {auction.market_id} not closed")
        logging.error(e)
        db.session.rollback()


def check_expired_auctions():
    logging.info("Running task to check expired auctions...")
    expired_auctions = Market.query.filter(
        Market.end_date <= datetime.utcnow(), Market.status == "open"
    ).all()
    for auction in expired_auctions:
        handle_expired_auction(auction)
