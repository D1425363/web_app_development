# 路由與頁面設計文件 (ROUTES)

本文件依據 PRD、系統架構 (ARCHITECTURE) 與資料庫設計 (DB_DESIGN)，規劃個人記帳簿 Flask 應用程式的路由設計。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| 首頁 (統計總覽) | GET | `/` | `templates/index.html` | 顯示當月總收入、總支出、結餘與最近幾筆明細 |
| 收支明細列表 | GET | `/transactions` | `templates/list.html` | 顯示所有歷史記帳明細列表，並包含新增表單 |
| 建立收支紀錄 | POST | `/transactions` | — | 接收新增表單，存入 DB，完成後重導向至列表頁 |
| 編輯收支頁面 | GET | `/transactions/<int:id>/edit` | `templates/edit.html` | 顯示特定收支紀錄的編輯表單 |
| 更新收支紀錄 | POST | `/transactions/<int:id>/update` | — | 接收編輯表單，更新 DB，完成後重導向至列表頁 |
| 刪除收支紀錄 | POST | `/transactions/<int:id>/delete` | — | 刪除指定收支紀錄，完成後重導向至列表頁 |

## 2. 每個路由的詳細說明

### 首頁 (統計總覽)
*   **路由**: `GET /`
*   **輸入**: 無
*   **處理邏輯**: 呼叫 `Transaction` Model 計算當月總收入、總支出與結餘，並取得最近幾筆 (例如 5 筆) 歷史紀錄。
*   **輸出**: 渲染 `index.html`，傳入統計資料與近期紀錄。
*   **錯誤處理**: 若資料庫讀取錯誤，顯示適當錯誤訊息。

### 收支明細列表 (包含新增表單)
*   **路由**: `GET /transactions`
*   **輸入**: 選擇性的查詢參數 (例如：月份篩選，預留擴充)。
*   **處理邏輯**: 呼叫 `Transaction.get_all()` 取得所有歷史明細。
*   **輸出**: 渲染 `list.html`，傳入所有明細列表資料。此頁面亦包含新增紀錄的 HTML 表單。
*   **錯誤處理**: 若無資料則顯示「目前尚無紀錄」。

### 建立收支紀錄
*   **路由**: `POST /transactions`
*   **輸入**: 表單欄位包含 `type` (income/expense), `amount` (float), `category` (string), `date` (YYYY-MM-DD), `note` (string, optional)。
*   **處理邏輯**: 驗證表單輸入，若合法則呼叫 `Transaction.create()` 寫入資料庫。
*   **輸出**: 成功後重導向 (Redirect) 至 `/transactions`。
*   **錯誤處理**: 若輸入無效 (如金額非數字、必填欄位為空)，可重導向回列表頁並附帶錯誤訊息 (Flash messages)。

### 編輯收支頁面
*   **路由**: `GET /transactions/<int:id>/edit`
*   **輸入**: URL 參數 `id`。
*   **處理邏輯**: 呼叫 `Transaction.get_by_id(id)` 取得該筆紀錄詳細資料。
*   **輸出**: 渲染 `edit.html`，將取得的紀錄填入表單作為預設值。
*   **錯誤處理**: 若 `id` 不存在，回傳 404 錯誤頁面或重導向並顯示錯誤訊息。

### 更新收支紀錄
*   **路由**: `POST /transactions/<int:id>/update`
*   **輸入**: URL 參數 `id`，以及表單更新後的 `type`, `amount`, `category`, `date`, `note`。
*   **處理邏輯**: 驗證表單輸入，合法則呼叫 `Transaction.update(id, data)`。
*   **輸出**: 成功後重導向至 `/transactions`。
*   **錯誤處理**: 表單驗證失敗時，重導向回編輯頁面並顯示錯誤。找不到 `id` 則回傳 404。

### 刪除收支紀錄
*   **路由**: `POST /transactions/<int:id>/delete`
*   **輸入**: URL 參數 `id`。
*   **處理邏輯**: 呼叫 `Transaction.delete(id)` 從資料庫移除該筆資料。
*   **輸出**: 成功後重導向至 `/transactions`。
*   **錯誤處理**: 若 `id` 不存在，重導向並提示錯誤。

## 3. Jinja2 模板清單

所有的模板檔案皆位於 `app/templates/` 之下，並繼承共用的基礎版型。

*   **`base.html`**:
    *   全站共用的基礎版型 (Base Template)。
    *   包含 HTML 骨架、`<head>` (匯入自訂的 CSS 與 Google Fonts)、全域導覽列 (Navbar) 與頁尾 (Footer)。
    *   定義 `{% block content %}{% endblock %}` 供子模板填入內容。
*   **`index.html`**:
    *   首頁統計與總覽頁面。
    *   繼承自 `base.html`。
    *   主要區塊：當月餘額卡片、收支圓餅圖 (預留給 JS)、最近明細小聚落。
*   **`list.html`**:
    *   明細列表與新增頁面。
    *   繼承自 `base.html`。
    *   主要區塊：上方為「新增收支表單」，下方為「歷史收支明細表格」。
*   **`edit.html`**:
    *   編輯收支頁面 (擴充自架構文件，確保編輯有獨立且乾淨的版面)。
    *   繼承自 `base.html`。
    *   主要區塊：包含預填原有資料的表單，讓使用者修改後送出更新。

## 4. 路由骨架程式碼規劃

對應到 `app/routes/` 的 Python 檔案：

*   **`app/routes/index.py`**: 包含首頁相關邏輯。
*   **`app/routes/transaction_routes.py`**: 包含所有 `Transaction` 的 CRUD 路由。
*   **`app/routes/__init__.py`**: 用於註冊所有 Blueprint 或是載入各路由檔案，以利 `app.py` 匯入。
