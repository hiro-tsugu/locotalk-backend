import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    # ローカル or Azure の判別用
    is_azure = 'WEBSITE_INSTANCE_ID' in os.environ

    if is_azure:
        ssl_cert_path = '/home/site/wwwroot/certs/BaltimoreCyberTrustRoot.crt.pem'
    else:
        ssl_cert_path = os.path.join(os.getcwd(), 'certs', 'BaltimoreCyberTrustRoot.crt.pem')

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
