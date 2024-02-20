from flask import Flask, request, jsonify
import os
from dotenv.main import load_dotenv
import mysql.connector
import re

load_dotenv()
app = Flask(__name__)

user = os.environ['USER']
password = os.environ['PASSWORD']
host = os.environ['HOST']

connect = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database="getcontact"
)
cursor = connect.cursor()


cursor.execute("""CREATE TABLE IF NOT EXISTS numbers(
   id BIGINT NOT NULL PRIMARY KEY,
   numbuster TEXT,
   getcontact TEXT
   );
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
   id BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
   name VARCHAR(255) NOT NULL,
   date DATETIME
)
""")

connect.commit()
cursor.close()
connect.close()


@app.route('/api', methods=['POST'])
def index():
    number = request.form['number']

    connect = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database="getcontact"
    )
    c = connect.cursor()

    number = re.sub(r'^(\+7|8)', '7', number)
    c.execute(
        "SELECT numbuster, getcontact FROM numbers WHERE id = %s",
        (number,))
    value = c.fetchall()
    if value != []:
        return jsonify(value)
    else:
        return {}


if __name__ == '__main__':
    app.run(port=6666,)
