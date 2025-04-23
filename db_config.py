import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
        charset='utf8',
        ssl_ca=os.path.join(os.getcwd(), 'BaltimoreCyberTrustRoot.crt.pem'),
        ssl_verify_cert=True
    )
