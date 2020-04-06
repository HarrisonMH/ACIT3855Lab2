import mysql.connector

# db_conn = mysql.connector.connect(host="localhost", user="root", password="P@ssw0rd", database="orders")
db_conn = mysql.connector.connect(host="acit3855-a00875065.eastus2.cloudapp.azure.com", user="root", password="password", database="orders")


db_cursor = db_conn.cursor()

db_cursor.execute('''
          CREATE TABLE delivery_orders
          (id INT NOT NULL AUTO_INCREMENT, 
           restaurant_id VARCHAR(250) NOT NULL,
           user_id VARCHAR(250) NOT NULL,
           order_details VARCHAR(10000) NOT NULL,
           order_time DATETIME NOT NULL,
           date_created DATETIME NOT NULL,
           CONSTRAINT delivery_orders_pk PRIMARY KEY (id)
          ) ''')

db_cursor.execute('''
          CREATE TABLE pickup_orders
          (id INT NOT NULL AUTO_INCREMENT, 
           restaurant_id VARCHAR(250) NOT NULL,
           user_id VARCHAR(250) NOT NULL,
           order_details VARCHAR(10000) NOT NULL,
           order_time DATETIME NOT NULL,
           date_created DATETIME NOT NULL,
           CONSTRAINT pickup_orders_pk PRIMARY KEY (id)
          ) ''')

db_conn.commit()
db_conn.close()


