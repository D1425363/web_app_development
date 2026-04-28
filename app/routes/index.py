from flask import render_template
from . import index_bp
from app.models import Transaction
from datetime import datetime

@index_bp.route('/')
def home():
    """
    首頁路由 (GET /)
    
    處理邏輯：
    1. 計算當月總收入、總支出與結餘。
    2. 取得最近幾筆 (例如 5 筆) 歷史明細。
    
    輸出：
    渲染 `index.html`，傳入統計資料與近期紀錄。
    """
    try:
        transactions = Transaction.get_all()
    except Exception:
        transactions = []
        
    current_month_str = datetime.now().strftime('%Y-%m')
    
    total_income = 0.0
    total_expense = 0.0
    
    # 統計當月的收支
    for t in transactions:
        if t['date'].startswith(current_month_str):
            if t['type'] == 'income':
                total_income += t['amount']
            elif t['type'] == 'expense':
                total_expense += t['amount']
                
    balance = total_income - total_expense
    
    # 取得最近 5 筆
    recent_transactions = transactions[:5]
    
    return render_template(
        'index.html',
        total_income=total_income,
        total_expense=total_expense,
        balance=balance,
        recent_transactions=recent_transactions,
        current_month=current_month_str
    )
