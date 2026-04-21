import sqlite3

# 資料庫檔案位置設定，基於 instance 目錄分離
DATABASE = 'instance/database.db'

def get_db_connection():
    """與 SQLite 建立連線並設定 row_factory，方便透過欄位名稱存取"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

class Transaction:
    @staticmethod
    def create(type, amount, category, date, note=""):
        """新增一筆收支紀錄"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO transactions (type, amount, category, date, note)
            VALUES (?, ?, ?, ?, ?)
        ''', (type, amount, category, date, note))
        conn.commit()
        last_id = cursor.lastrowid
        conn.close()
        return last_id

    @staticmethod
    def get_all():
        """取得所有收支紀錄，並依日期排序 (越新越前面)"""
        conn = get_db_connection()
        transactions = conn.execute('SELECT * FROM transactions ORDER BY date DESC, id DESC').fetchall()
        conn.close()
        return transactions

    @staticmethod
    def get_by_id(transaction_id):
        """依據 ID 取得單筆資料"""
        conn = get_db_connection()
        transaction = conn.execute('SELECT * FROM transactions WHERE id = ?', (transaction_id,)).fetchone()
        conn.close()
        return transaction

    @staticmethod
    def update(transaction_id, type, amount, category, date, note=""):
        """更新單筆收支資料"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE transactions
            SET type = ?, amount = ?, category = ?, date = ?, note = ?
            WHERE id = ?
        ''', (type, amount, category, date, note, transaction_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(transaction_id):
        """刪除單筆收支紀錄"""
        conn = get_db_connection()
        conn.execute('DELETE FROM transactions WHERE id = ?', (transaction_id,))
        conn.commit()
        conn.close()
