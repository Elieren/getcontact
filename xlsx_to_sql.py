import pandas as pd
import json
import sqlite3
import re


connect = sqlite3.connect('base.db')  # Database creation
cursor = connect.cursor()


# phone_clear;numbuster;getcontact


cursor.execute("""CREATE TABLE IF NOT EXISTS numbers(
   id INTEGER NOT NULL PRIMARY KEY,
   numbuster TEXT,
   getcontact TEXT
   );
""")

connect.commit()


# Загрузите данные из xlsx файла
df = pd.read_excel('Getcontact lSECURITYl.xlsx')

# Переберите столбцы в DataFrame
for column in df.columns:
    x = df[column]

list_numb = []

for z, i in enumerate(x[2:-1]):
    try:
        print(z, i)
        i = i.replace('\\;', ' ')
        lst = i.split(';')
        if lst[1] != 'NULL':
            lst[1] = lst[1].replace('\\\\\\"', '\"')
            try:
                k = json.loads(lst[1])
            except Exception:
                lst[1] = lst[1].replace('\\\\"', '')
                k = json.loads(lst[1])

            for y, i in enumerate(k):
                k[y] = re.sub(r'[^a-zA-Zа-яА-Я .0-9-()]', '', i)

            lst[1] = ',\n'.join(k)
        if lst[2] != 'NULL':
            lst[2] = lst[2].replace('\\\\\\"', '\"')
            try:
                k = json.loads(lst[2])
            except Exception:
                lst[2] = lst[2].replace('\\\\"', '')
                k = json.loads(lst[2])

            for y, i in enumerate(k):
                k[y] = re.sub(r'[^a-zA-Zа-яА-Я .0-9-()]', '', i)

            lst[2] = ',\n'.join(k)
    except Exception as e:
        print(e)

    try:
        cursor.execute("INSERT INTO numbers VALUES (?, ?, ?)", (
            lst[0], lst[1], lst[2]))
        connect.commit()
    except Exception:
        pass
