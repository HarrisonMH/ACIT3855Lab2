import sqlite3

conn = sqlite3.connect('orders.sqlite')

c = conn.cursor()
c.execute('''
          CREATE TABLE delivery_orders
          (id INTEGER PRIMARY KEY ASC, 
           restaurant_id VARCHAR(250) NOT NULL,
           user_id VARCHAR(250) NOT NULL,
           order_details VARCHAR(10000) NOT NULL,
           order_time DATE NOT NULL,
           date_created DATE NOT NULL
          ); ''')

c.execute('''
          CREATE TABLE pickup_orders
          (id INTEGER PRIMARY KEY ASC, 
           restaurant_id VARCHAR(250) NOT NULL,
           user_id VARCHAR(250) NOT NULL,
           order_details VARCHAR(10000) NOT NULL,
           order_time DATE NOT NULL,
           date_created DATE NOT NULL
          ); ''')

conn.commit()
conn.close()


