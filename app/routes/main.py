from flask import Blueprint, render_template
from app.models.record import RecordModel

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def index():
    """
    顯示首頁 (明細清單)。
    - 取得所有收支紀錄。
    - 計算總收支、餘額。
    - 將資料傳遞給 templates/index.html 進行渲染。
    """
    records = RecordModel.get_all()
    
    total_income = sum(r['amount'] for r in records if r['type'] == 'income')
    total_expense = sum(r['amount'] for r in records if r['type'] == 'expense')
    balance = total_income - total_expense

    return render_template('index.html', 
                           records=records, 
                           total_income=total_income, 
                           total_expense=total_expense, 
                           balance=balance)
