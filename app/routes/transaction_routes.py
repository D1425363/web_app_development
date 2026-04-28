from flask import render_template, request, redirect, url_for, flash
from . import transaction_bp

@transaction_bp.route('/transactions', methods=['GET'])
def list_transactions():
    """
    收支明細列表 (GET /transactions)
    
    處理邏輯：
    取得所有歷史明細。此頁面同時包含新增紀錄的表單。
    
    輸出：
    渲染 `list.html`，傳入所有明細資料。
    """
    pass

@transaction_bp.route('/transactions', methods=['POST'])
def create_transaction():
    """
    建立收支紀錄 (POST /transactions)
    
    處理邏輯：
    接收表單資料 (type, amount, category, date, note)。
    驗證通過後存入資料庫。
    
    輸出：
    成功後重導向至 `/transactions` 列表頁。
    若驗證失敗，顯示錯誤訊息。
    """
    pass

@transaction_bp.route('/transactions/<int:id>/edit', methods=['GET'])
def edit_transaction(id):
    """
    編輯收支頁面 (GET /transactions/<id>/edit)
    
    處理邏輯：
    依據 ID 取得特定收支紀錄資料。
    
    輸出：
    渲染 `edit.html`，將取得的紀錄作為預設值填入表單。
    """
    pass

@transaction_bp.route('/transactions/<int:id>/update', methods=['POST'])
def update_transaction(id):
    """
    更新收支紀錄 (POST /transactions/<id>/update)
    
    處理邏輯：
    接收表單更新資料。
    驗證通過後依據 ID 更新資料庫紀錄。
    
    輸出：
    成功後重導向至 `/transactions` 列表頁。
    """
    pass

@transaction_bp.route('/transactions/<int:id>/delete', methods=['POST'])
def delete_transaction(id):
    """
    刪除收支紀錄 (POST /transactions/<id>/delete)
    
    處理邏輯：
    依據 ID 從資料庫移除該筆資料。
    
    輸出：
    成功後重導向至 `/transactions` 列表頁。
    """
    pass
