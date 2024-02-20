import sqlite3
import mysql.connector
from dotenv.main import load_dotenv
import os


load_dotenv()
token = os.environ['TOKEN']
user = os.environ['USER']
password = os.environ['PASSWORD']
host = os.environ['HOST']

connect = sqlite3.connect('base.db')  # Database creation
cursor = connect.cursor()

connect_my = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database="getcontact"
)
cursor_my = connect_my.cursor()

cursor_my.execute("""CREATE TABLE IF NOT EXISTS numbers(
   id BIGINT NOT NULL PRIMARY KEY,
   numbuster TEXT,
   getcontact TEXT
   );
""")

connect_my.commit()

cursor.execute("SELECT * FROM numbers")
value = cursor.fetchall()
for i in value:
    try:
        cursor_my.execute("INSERT INTO numbers VALUES(%s, %s, %s)",
                          (i[0], i[1], i[2]))
        connect_my.commit()
        print('+', i[0])
    except Exception:
        print('-', i[0])

cursor_my.close()
connect_my.close()
