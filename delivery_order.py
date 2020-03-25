from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime


class DeliveryOrder(Base):
    """ Delivery Order """

    __tablename__ = "delivery_orders"

    id = Column(Integer, primary_key=True)
    restaurant_id = Column(String(250), nullable=False)
    user_id = Column(String(250), nullable=False)
    order_details = Column(String(10000), nullable=False)
    order_time = Column(DateTime, nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(self, restaurant_id, user_id, order_details, order_time):
        """ Initializes a delivery order """
        self.restaurant_id = restaurant_id
        self.user_id = user_id
        self.order_details = order_details
        self.order_time = order_time
        self.date_created = datetime.datetime.now()

    def to_dict(self):
        """ Dictionary Representation of a pickup order """
        dict = {}
        dict['id'] = self.id
        dict['restaurant_id'] = self.restaurant_id
        dict['user_id'] = self.user_id
        dict['order_details'] = self.order_details
        dict['order_time'] = self.order_time

        return dict
