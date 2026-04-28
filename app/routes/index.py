from flask import render_template
from . import index_bp

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
    pass
