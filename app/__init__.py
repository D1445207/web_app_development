import os
from flask import Flask

def create_app(test_config=None):
    # 建立與設定 app
    app = Flask(__name__, instance_relative_config=True)
    
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        DATABASE=os.path.join(app.instance_path, 'database.db'),
    )

    if test_config is None:
        # 當不測試時載入設定檔 (若存在)
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # 確保 instance 目錄存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 在應用程式環境中初始化資料庫
    with app.app_context():
        from app.models.record import RecordModel
        RecordModel.init_db()

    # 註冊所有的 Blueprint 路由
    from app.routes import register_blueprints
    register_blueprints(app)

    return app
