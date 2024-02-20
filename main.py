from telebot.async_telebot import AsyncTeleBot
from dotenv.main import load_dotenv
import os
import mysql.connector
from datetime import datetime
import asyncio
import re

load_dotenv()
token = os.environ['TOKEN']
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

bot = AsyncTeleBot(token)


async def is_phone_number(phone_number):
    pattern = r'^(7|8|\+7)\d{10}$'
    return bool(re.match(pattern, phone_number))


async def convert_phone_number(phone_number):
    return re.sub(r'^(\+7|8)', '7', phone_number)


@bot.message_handler(commands=["start"])
async def start(message):
    await bot.send_message(
        message.chat.id,
        'Hello\nОтправьте мне номер телефона.')
    try:
        connect = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database="getcontact"
        )
        c = connect.cursor()
        c.execute("INSERT INTO users VALUES(%s, %s, %s)",
                  (message.chat.id, message.from_user.full_name,
                   datetime.now()))
        connect.commit()
    except Exception:
        pass

    c.close()
    connect.close()


@bot.message_handler(content_types=["text"])
async def handle_message(message):
    # try:
    connect = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database="getcontact"
    )
    c = connect.cursor()

    number = message.text
    x = await is_phone_number(number)
    if x:
        number = await convert_phone_number(number)
        c.execute(
            "SELECT numbuster, getcontact FROM numbers WHERE id = %s",
            (number,))
        value = c.fetchall()
        if value != []:
            text = f'📱Number: {number}\n\n'
            text += f'Numbuster:\n\n{value[0][0]}\n'
            text += f'\nGetcontact:\n\n{value[0][1]}'
            await bot.send_message(message.chat.id, text)
        else:
            await bot.send_message(
                message.chat.id,
                "Такого номера в базе данных нет.")
    else:
        await bot.send_message(message.chat.id,
                               'Не верный номер телефона.')

    # except Exception:
    #     pass

    c.close()
    connect.close()

if __name__ == '__main__':

    print('SERVER START')
    asyncio.run(bot.polling(none_stop=True))
