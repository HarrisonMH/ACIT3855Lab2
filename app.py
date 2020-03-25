# app.py
#
# Main app definition
#
# Author: Matt Harrison, Set 4B, A00875065

# Date example: 2020-01-22T22:00:00Z

import connexion
from connexion import NoContent
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from pickup_order import PickupOrder
from delivery_order import DeliveryOrder
import datetime
import json
import yaml
from threading import Thread
from pykafka import KafkaClient
import logging
import logging.config

# DB_ENGINE = create_engine('sqlite:///orders.sqlite')

with open('app_conf.yaml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yaml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

DB_ENGINE = create_engine('mysql+pymysql://%s:%s@%s:%s/%s' %
                          (app_config["datastore"]["user"], app_config["datastore"]["password"],
                           app_config["datastore"]["hostname"], app_config["datastore"]["port"],
                           app_config["datastore"]["db"]))

Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)
DATE_FORMAT_STR = "%Y-%m-%dT%H:%M:%SZ"


# Functions
# def add_pickup(**test_params):
#     """ Receives a pickup order request"""
#     session = DB_SESSION()
#     order_data = test_params["body"]
#
#     new_order = PickupOrder(order_data["restaurant_id"],
#                             order_data["user_id"],
#                             json.dumps(order_data["order_details"]),
#                             datetime.datetime.strptime(order_data["order_time"], DATE_FORMAT_STR))
#     session.add(new_order)
#     session.commit()
#     session.close()
#
#     return NoContent, 200
#
#
# def add_delivery(**test_params):
#     """ Receives a delivery order request"""
#     session = DB_SESSION()
#     order_data = test_params["body"]
#
#     new_order = DeliveryOrder(order_data["restaurant_id"],
#                             order_data["user_id"],
#                             json.dumps(order_data["order_details"]),
#                             datetime.datetime.strptime(order_data["order_time"], DATE_FORMAT_STR))
#     session.add(new_order)
#     session.commit()
#     session.close()
#     return NoContent, 200


def consume_pickup(order_details, offset):
    session = DB_SESSION()
    new_order = PickupOrder(order_details["restaurant_id"],
                            order_details["user_id"],
                            json.dumps(order_details["order_details"]),
                            datetime.datetime.strptime(order_details["order_time"], DATE_FORMAT_STR))
    session.add(new_order)
    session.commit()
    session.close()
    logger.debug("Consumed pickup order %s: %s" % (offset, order_details))
    return


def consume_delivery(order_details, offset):
    session = DB_SESSION()
    new_order = DeliveryOrder(order_details["restaurant_id"],
                              order_details["user_id"],
                              json.dumps(order_details["order_details"]),
                              datetime.datetime.strptime(order_details["order_time"], DATE_FORMAT_STR))
    session.add(new_order)
    session.commit()
    session.close()
    print("Consumed delivery order %s: %s" % (offset, order_details))
    return


def get_pickup(startDate, endDate):
    """ Retrieves a list of pickup orders between specified dates """
    results_list = []
    session = DB_SESSION()

    query = (session.query(PickupOrder)
             .filter(PickupOrder.date_created >= datetime.datetime.strptime(startDate, DATE_FORMAT_STR))
             .filter(PickupOrder.date_created <= datetime.datetime.strptime(endDate, DATE_FORMAT_STR)))

    for result in query:
        results_list.append(result.to_dict())

    session.close()
    logger.debug("Retrieved pickup orders between %s and %s" % (startDate, endDate))

    return results_list, 200


def get_delivery(startDate, endDate):
    """ Retrieves a list of delivery orders between specified dates """
    results_list = []
    session = DB_SESSION()

    query = (session.query(DeliveryOrder)
             .filter(DeliveryOrder.date_created >= datetime.datetime.strptime(startDate, DATE_FORMAT_STR))
             .filter(DeliveryOrder.date_created <= datetime.datetime.strptime(endDate, DATE_FORMAT_STR)))

    for result in query:
        results_list.append(result.to_dict())

    session.close()
    logger.debug("Retrieved delivery orders between %s and %s" % (startDate, endDate))

    return results_list, 200


def process_messages():
    client = KafkaClient(hosts=app_config["kafka"]["server"] + ':' + str(app_config["kafka"]["port"]))
    topic = client.topics[app_config["kafka"]["topic"]]
    consumer = topic.get_simple_consumer(consumer_group="order_group", auto_commit_enable=True, auto_commit_interval_ms=1000)

    # This is blocking - it will wait for a new message
    for msg in consumer:
        msg_str = msg.value.decode('utf-8')
        msg_dict = json.loads(msg_str)
        # Check the type and add to the DB
        if msg_dict["type"] == "pickup_order":
            consume_pickup(msg_dict["payload"], msg.offset)
            logger.info("Committing pickup order to database: %s" % msg_dict)
        elif msg_dict["type"] == "delivery_order":
            consume_delivery(msg_dict["payload"], msg.offset)
            logger.info("Committing delivery order to database: %s" % msg_dict)


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml")

if __name__ == "__main__":
    t1 = Thread(target=process_messages)
    t1.setDaemon(True)
    t1.start()
    app.run(host="127.0.0.1", port=8090)
