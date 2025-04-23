from flask import Blueprint, request, jsonify
from db_config import get_connection  # ← 修正点：pymysql ではなく db_config を使用

municipality_bp = Blueprint('municipality_bp', __name__)

@municipality_bp.route('/municipalities', methods=['GET'])
def get_all_municipalities():
    conn = None
    cursor = None
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
    conn = None
    cursor = None
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
        print(f"❌ [municipality.py] ID検索エラー: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
