from flask import Blueprint, jsonify
from db_config import get_connection

municipality_bp = Blueprint('municipality', __name__, url_prefix='/api')

@municipality_bp.route('/municipality/<id>', methods=['GET'])
def get_municipality(id):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT id, prefecture, jurisdiction, city, sub_city, name, created_at
            FROM municipalities
            WHERE id = %s
        """, (id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if result:
            return jsonify(result), 200
        else:
            return jsonify({'message': 'Municipality not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
