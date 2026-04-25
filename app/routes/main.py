from flask import Blueprint

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def index():
    """
    顯示首頁 (明細清單)。
    - 取得所有收支紀錄。
    - 計算總收支、餘額。
    - 將資料傳遞給 templates/index.html 進行渲染。
    """
    pass
