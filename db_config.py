import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    ssl_cert_path = os.path.join(os.getcwd(), 'BaltimoreCyberTrustRoot.crt.pem')
    print("🔍 SSL証明書パス:", ssl_cert_path)  # ★ この行でパスを出力

    try:
        conn = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE"),
            charset='utf8',
            ssl_ca = os.path.join(os.getcwd(), 'certs', 'BaltimoreCyberTrustRoot.crt.pem'),
            ssl_verify_cert=True
        )
        print("✅ DB接続成功")
        return conn
    except Exception as e:
        print("❌ DB接続エラー:", e)  # ★ エラー詳細も出力
        raise
