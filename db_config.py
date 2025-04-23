import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    # Azure 上のアプリルート固定パスを使用
    ssl_cert_path = '/home/site/wwwroot/certs/BaltimoreCyberTrustRoot.crt.pem'
    
    print("🔍 使用証明書ファイル:", ssl_cert_path)
    print("🔍 存在確認:", os.path.exists(ssl_cert_path))

    try:
        conn = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE"),
            charset='utf8',
            ssl_ca=ssl_cert_path,
            ssl_verify_cert=True
        )
        print("✅ DB接続成功")
        return conn
    except Exception as e:
        print("❌ DB接続エラー:", e)
        raise

