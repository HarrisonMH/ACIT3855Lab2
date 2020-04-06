import mysql.connector

conn = mysql.connector.connect(host="acit3855-a00875065.eastus2.cloudapp.azure.com", user="root", password="password")

db_cursor = conn.cursor()

db_cursor.execute('''
    CREATE DATABASE orders;
''')

conn.commit()
conn.close()


