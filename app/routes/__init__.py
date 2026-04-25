from .main import main_bp
from .records import records_bp

def register_blueprints(app):
    """將所有 routing blueprints 註冊到 main Flask app"""
    app.register_blueprint(main_bp)
    app.register_blueprint(records_bp)
