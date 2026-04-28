from flask import render_template, request, redirect, url_for, flash
from . import transaction_bp
from app.models import Transaction

@transaction_bp.route('/transactions', methods=['GET'])
def list_transactions():
    """
    收支明細列表 (GET /transactions)
    """
    try:
        transactions = Transaction.get_all()
    except Exception:
        flash("無法讀取收支明細，請稍後再試。", "error")
        transactions = []
        
    return render_template('list.html', transactions=transactions)

@transaction_bp.route('/transactions', methods=['POST'])
def create_transaction():
    """
    建立收支紀錄 (POST /transactions)
    """
    type_val = request.form.get('type')
    amount_str = request.form.get('amount')
    category = request.form.get('category')
    date_val = request.form.get('date')
    note = request.form.get('note', '')
    
    # 基本驗證：必填欄位檢查
    if not all([type_val, amount_str, category, date_val]):
        flash('請填寫所有必填欄位 (類型、金額、分類、日期)', 'error')
        return redirect(url_for('transaction.list_transactions'))
        
    # 基本驗證：金額格式檢查
    try:
        amount = float(amount_str)
    except ValueError:
        flash('金額必須為數字', 'error')
        return redirect(url_for('transaction.list_transactions'))
        
    data = {
        'type': type_val,
        'amount': amount,
        'category': category,
        'date': date_val,
        'note': note
    }
    
    # 儲存至資料庫
    try:
        Transaction.create(data)
        flash('新增收支成功！', 'success')
    except Exception:
        flash('新增記錄發生錯誤，請稍後再試。', 'error')
        
    return redirect(url_for('transaction.list_transactions'))

@transaction_bp.route('/transactions/<int:id>/edit', methods=['GET'])
def edit_transaction(id):
    """
    編輯收支頁面 (GET /transactions/<id>/edit)
    """
    try:
        transaction = Transaction.get_by_id(id)
        if not transaction:
            flash('找不到該筆紀錄', 'error')
            return redirect(url_for('transaction.list_transactions'))
    except Exception:
        flash('讀取紀錄時發生錯誤', 'error')
        return redirect(url_for('transaction.list_transactions'))
        
    return render_template('edit.html', transaction=transaction)

@transaction_bp.route('/transactions/<int:id>/update', methods=['POST'])
def update_transaction(id):
    """
    更新收支紀錄 (POST /transactions/<id>/update)
    """
    type_val = request.form.get('type')
    amount_str = request.form.get('amount')
    category = request.form.get('category')
    date_val = request.form.get('date')
    note = request.form.get('note', '')
    
    # 必填欄位檢查
    if not all([type_val, amount_str, category, date_val]):
        flash('請填寫所有必填欄位', 'error')
        return redirect(url_for('transaction.edit_transaction', id=id))
        
    # 金額格式檢查
    try:
        amount = float(amount_str)
    except ValueError:
        flash('金額必須為數字', 'error')
        return redirect(url_for('transaction.edit_transaction', id=id))
        
    data = {
        'type': type_val,
        'amount': amount,
        'category': category,
        'date': date_val,
        'note': note
    }
    
    # 更新資料庫
    try:
        success = Transaction.update(id, data)
        if success:
            flash('更新收支成功！', 'success')
        else:
            flash('更新失敗，找不到該筆紀錄', 'error')
    except Exception:
        flash('更新記錄發生錯誤，請稍後再試。', 'error')
        return redirect(url_for('transaction.edit_transaction', id=id))
        
    return redirect(url_for('transaction.list_transactions'))

@transaction_bp.route('/transactions/<int:id>/delete', methods=['POST'])
def delete_transaction(id):
    """
    刪除收支紀錄 (POST /transactions/<id>/delete)
    """
    try:
        success = Transaction.delete(id)
        if success:
            flash('刪除成功！', 'success')
        else:
            flash('刪除失敗，找不到該筆紀錄', 'error')
    except Exception:
        flash('刪除記錄時發生錯誤。', 'error')
        
    return redirect(url_for('transaction.list_transactions'))
