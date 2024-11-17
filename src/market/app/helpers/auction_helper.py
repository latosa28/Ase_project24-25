import logging
from datetime import datetime
import requests
from flask import current_app

from models.models import Market, db


def add_amount(user_id, amount):
    response = requests.post(
        current_app.config["currency"] + f"/user/{user_id}/add_amount",
        json={"amount": str(amount)},
    )
    if response.status_code != 200:
        raise Exception("Seller doesn't obtain the amount of the auction")


def move_instance(user_id, new_user_id, istance_id):
    response = requests.post(
        current_app.config["collection"] + f"/user/{user_id}/instance/{istance_id}",
        json={"new_user_id": new_user_id},
    )
    if response.status_code != 200:
        raise Exception("Buyer doesn't obtain the istance")


def handle_expired_auction(auction):
    try:
        logging.info(f"Auction {auction.market_id} has expired, processing...")
        auction.status = "expired"
        if auction.seller_user_id:
            add_amount(auction.seller_user_id, auction.bid)
            move_instance(
                auction.seller_user_id, auction.buyer_user_id, auction.istance_id
            )
            db.session.commit()
            logging.info(f"Auction {auction.market_id} closed successfully.")
    except Exception as e:
        logging.error(f"Auction {auction.market_id} not closed")
        db.session.rollback()


def check_expired_auctions():
    logging.info("Running task to check expired auctions...")
    expired_auctions = Market.query.filter(
        Market.end_date <= datetime.utcnow(), Market.status == "open"
    ).all()
    for auction in expired_auctions:
        handle_expired_auction(auction)
