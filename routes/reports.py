from flask import Blueprint, request, jsonify
from db_config import get_connection
from datetime import datetime
import base64
import traceback

report_bp = Blueprint('reports', __name__)

# レポート取得
@report_bp.route('/reports', methods=['GET'])
def get_reports():
    try:
        municipality_id = request.args.get('municipality_id')
        if not municipality_id:
            return jsonify({'error': 'municipality_id is required'}), 400

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT r.id, r.title, r.body, r.created_at, i.image_data, u.nickname
            FROM reports r
            LEFT JOIN images i ON r.image_id = i.id
            LEFT JOIN users u ON r.user_id = u.id
            WHERE r.municipality_id = %s
            ORDER BY r.created_at DESC
        """
        cursor.execute(query, (municipality_id,))
        rows = cursor.fetchall()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

    reports = []
    for row in rows:
        image_base64 = None
        if row['image_data']:
            image_base64 = base64.b64encode(row['image_data']).decode('utf-8')
        reports.append({
            'id': row['id'],
            'title': row['title'],
            'body': row['body'],
            'created_at': row['created_at'],
            'nickname': row['nickname'],
            'image_data': image_base64
        })

    return jsonify(reports)


# レポート投稿
@report_bp.route('/reports', methods=['POST'])
def post_report():
    try:
        user_id = request.form.get('user_id')
        municipality_id = request.form.get('municipality_id')
        title = request.form.get('title')
        body = request.form.get('body')
        image_file = request.files.get('image')
        image_id = None

        conn = get_connection()
        cursor = conn.cursor()

        if image_file and image_file.filename != '':
            image_data = image_file.read()
            cursor.execute(
                "INSERT INTO images (image_data, created_at) VALUES (%s, %s)",
                (image_data, datetime.now())
            )
            image_id = cursor.lastrowid
            print("✅ 画像保存成功 image_id:", image_id)

        if image_id:
            cursor.execute("""
                INSERT INTO reports (user_id, municipality_id, title, body, image_id, created_at)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (user_id, municipality_id, title, body, image_id, datetime.now()))
        else:
            cursor.execute("""
                INSERT INTO reports (user_id, municipality_id, title, body, created_at)
                VALUES (%s, %s, %s, %s, %s)
            """, (user_id, municipality_id, title, body, datetime.now()))

        conn.commit()
        return jsonify({'message': '投稿が完了しました'}), 201

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()
