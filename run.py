from app import create_app
import os

app = create_app()

if __name__ == "__main__":
    # 讀取 .env 中的設定 (開發環境用)
    app.run(debug=True)
