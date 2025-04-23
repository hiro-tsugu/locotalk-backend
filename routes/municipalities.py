from flask import Blueprint, request, jsonify
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

municipality_bp = Blueprint('municipality_bp', __name__)

def get_connection():
    return pymysql.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        db=os.getenv("MYSQL_DATABASE"),
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

@municipality_bp.route('/municipalities', methods=['GET'])
def get_all_municipalities():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, prefecture, jurisdiction, city, sub_city, name, created_at
            FROM municipalities
            ORDER BY created_at DESC
        """)
        result = cursor.fetchall()
        return jsonify(result), 200
    except Exception as e:
        print(f"❌ [municipalities.py] DB接続エラー: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@municipality_bp.route('/municipality/<id>', methods=['GET'])
def get_municipality_by_id(id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM municipalities WHERE id = %s", (id,))
        result = cursor.fetchone()
        if result:
            return jsonify(result), 200
        else:
            return jsonify({'error': 'Municipality not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
