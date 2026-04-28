import os
from flask import Flask
from app.routes import register_routes
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

def create_app():
    app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
    
    # 基本設定
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    
    # 確保 instance 資料夾存在 (給 SQLite 使用)
    os.makedirs(app.instance_path, exist_ok=True)
    
    # 註冊所有的 Blueprint 路由
    register_routes(app)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
