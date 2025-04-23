import os
import requests
import json
from flask import Blueprint, request, jsonify, Response
from datetime import datetime

famous_bp = Blueprint('famous', __name__)

# 安定動作する推論APIモデルに変更
HF_API_URL = "https://api-inference.huggingface.co/models/prompthero/openjourney"
HF_API_KEY = os.getenv("HF_API_KEY")

OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def generate_prompt(prefecture, city):
    return f"""
以下は日本の自治体「{prefecture}{city}」に関する情報を返す形式です。

# 出力形式:
紹介文: 200次以内で自治体の特徴を細かく表現したわかりやすい紹介文。
名産品:
1. 名産品1
2. 名産品2
3. 名産品3
観光地:
1. 観光地1
2. 観光地2
3. 観光地3

では、{prefecture}{city}について上記の形式で出力してください。
""".strip()

@famous_bp.route('/api/famous', methods=['GET'])
def get_famous_info():
    prefecture = request.args.get('prefecture')
    city = request.args.get('city')

    if not prefecture or not city:
        return jsonify({'error': '都道府県または市区町村が指定されていません'}), 400

    print(f"✅ リクエスト受信：{prefecture} {city}")

    prompt = generate_prompt(prefecture, city)
    chat_response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
        },
    )

    if chat_response.status_code != 200:
        return jsonify({'error': 'ChatGPT APIエラー'}), 500

    text = chat_response.json()["choices"][0]["message"]["content"]
    lines = text.strip().splitlines()

    description = ""
    specialties = []
    sightseeing = []

    section = None
    for line in lines:
        line = line.strip()
        if line.startswith("紹介文:"):
            description = line.replace("紹介文:", "").strip()
            section = None
        elif line.startswith("名産品:"):
            section = "specialties"
        elif line.startswith("観光地:"):
            section = "sightseeing"
        elif line.startswith("1.") or line.startswith("2.") or line.startswith("3."):
            if section == "specialties":
                specialties.append(line[2:].strip())
            elif section == "sightseeing":
                sightseeing.append(line[2:].strip())

    # 画像生成処理
    image_url = None
    try:
        image_prompt = f"{prefecture}{city}の自然風景のイラストスタイル画像"
        image_response = requests.post(
            HF_API_URL,
            headers={
                "Authorization": f"Bearer {HF_API_KEY}",
                "Content-Type": "application/json"
            },
            json={"inputs": image_prompt}
        )

        if image_response.status_code == 200:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = f"static/generated_{prefecture}_{city}_{timestamp}.png"
            with open(filename, "wb") as f:
                f.write(image_response.content)
            image_url = "/" + filename
            print(f"📸 画像保存: {image_url}")
        else:
            print(f"画像生成APIエラー：{image_response.status_code}")
    except Exception as e:
        print(f"画像生成失敗: {e}")

    return Response(
    json.dumps({
        "name": f"{prefecture}{city}",
        "description": description,
        "specialties": specialties,
        "sightseeing": sightseeing,
        "image": image_url,
    }, ensure_ascii=False),  # ← 日本語をエスケープしない
    mimetype='application/json'
    )
