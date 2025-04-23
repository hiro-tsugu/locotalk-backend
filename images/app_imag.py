import mysql.connector
from datetime import datetime

# ← あなたのMySQL接続情報に置き換えてください
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Aina0803_Azumi0528',
    database='locotalk_db'
)

cursor = conn.cursor()

with open("sapporo.jpg", "rb") as f:
    img_data = f.read()

cursor.execute(
    "INSERT INTO images (image_data, created_at) VALUES (%s, %s)",
    (img_data, datetime.now())
)

conn.commit()
print("画像を保存しました。image_id:", cursor.lastrowid)

cursor.close()
conn.close()
