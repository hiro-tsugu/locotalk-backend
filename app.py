from flask import Flask
from flask_cors import CORS
from routes.municipalities import municipality_bp
from routes.reports import report_bp
from routes.famous import famous_bp  # ← 追加
from dotenv import load_dotenv  # ✅ 追加：.env 読み込みのため
import os  # ✅ 追加

load_dotenv()  # ✅ 追加：ルートの .env を一度だけ読み込む

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)

@app.route("/")
def index():
    return "Locotalk backend is running on Azure!"

# ファイルサイズの最大値設定（例：5MB）
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

app.register_blueprint(municipality_bp)
app.register_blueprint(report_bp)
app.register_blueprint(famous_bp)

print("✅ HF_API_KEY =", os.getenv("HF_API_KEY"))

if __name__ == '__main__':
    app.run(debug=True, port=5000)



