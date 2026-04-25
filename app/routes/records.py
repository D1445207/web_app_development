from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.record import RecordModel

records_bp = Blueprint('records', __name__)

@records_bp.route('/records/new', methods=['GET'])
def new_record():
    """
    顯示新增收支紀錄的表單頁面。
    - 準備並渲染 templates/form.html
    """
    return render_template('form.html', action='new')

@records_bp.route('/records', methods=['POST'])
def create_record():
    """
    接收表單並新增收支動作。
    - 取得 request.form 內的各項欄位參數
    - 呼叫 RecordModel.create() 新增紀錄至資料庫
    - 若成功，重導向至首頁 (main.index)
    """
    type = request.form.get('type')
    amount = request.form.get('amount')
    category = request.form.get('category')
    date = request.form.get('date')
    description = request.form.get('description', '')

    if not all([type, amount, category, date]):
        flash('請填寫所有必填欄位！', 'danger')
        return redirect(url_for('records.new_record'))

    try:
        data = {
            'type': type,
            'amount': float(amount),
            'category': category,
            'date': date,
            'description': description
        }
        RecordModel.create(data)
        flash('紀錄新增成功！', 'success')
        return redirect(url_for('main.index'))
    except Exception as e:
        flash(f'新增失敗: {e}', 'danger')
        return redirect(url_for('records.new_record'))

@records_bp.route('/records/<int:id>/edit', methods=['GET'])
def edit_record(id):
    """
    顯示編輯收支頁面。
    - 呼叫 RecordModel.get_by_id(id) 取得紀錄
    - 若不存在回傳 404
    - 將紀錄與 templates/form.html 一同渲染出來
    """
    record = RecordModel.get_by_id(id)
    if not record:
        flash('找不到該筆紀錄。', 'warning')
        return redirect(url_for('main.index'))
    return render_template('form.html', action='edit', record=record)

@records_bp.route('/records/<int:id>/update', methods=['POST'])
def update_record(id):
    """
    接收並更新收支動作。
    - 取得表單內容，準備更新
    - 呼叫 RecordModel.update() 更新資料庫
    - 重導向到首頁 (main.index)
    """
    type = request.form.get('type')
    amount = request.form.get('amount')
    category = request.form.get('category')
    date = request.form.get('date')
    description = request.form.get('description', '')

    if not all([type, amount, category, date]):
        flash('請填寫所有必填欄位！', 'danger')
        return redirect(url_for('records.edit_record', id=id))

    try:
        data = {
            'type': type,
            'amount': float(amount),
            'category': category,
            'date': date,
            'description': description
        }
        RecordModel.update(id, data)
        flash('紀錄更新成功！', 'success')
        return redirect(url_for('main.index'))
    except Exception as e:
        flash(f'更新失敗: {e}', 'danger')
        return redirect(url_for('records.edit_record', id=id))

@records_bp.route('/records/<int:id>/delete', methods=['POST'])
def delete_record(id):
    """
    刪除收支動作。
    - 呼叫 RecordModel.delete(id) 將資料自 DB 移除
    - 執行後重導向至首頁 (main.index)
    """
    try:
        RecordModel.delete(id)
        flash('紀錄已刪除。', 'success')
    except Exception as e:
        flash(f'刪除失敗: {e}', 'danger')
    
    return redirect(url_for('main.index'))
