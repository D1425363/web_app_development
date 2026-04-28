import sqlite3
import os
import logging

# 設定基礎的 log 記錄，用來記錄資料庫操作的錯誤
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# DB_PATH 預期會在 web_app_development/instance/database.db
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, 'instance', 'database.db')

def get_db_connection():
    """
    建立並回傳資料庫連線，設定 row_factory 讓結果可當作 dict (透過欄位名稱) 存取。
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        logger.error(f"資料庫連線錯誤: {e}")
        raise

class Transaction:
    @staticmethod
    def create(data):
        """
        新增一筆收支記錄。
        :param data: dict，包含 'type', 'amount', 'category', 'date', 'note'
        :return: int，新增記錄的 ID
        """
        query = '''
            INSERT INTO transactions (type, amount, category, date, note)
            VALUES (?, ?, ?, ?, ?)
        '''
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(query, (
                data.get('type'),
                data.get('amount'),
                data.get('category'),
                data.get('date'),
                data.get('note', '')
            ))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            logger.error(f"新增記錄失敗: {e}")
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                conn.close()

    @staticmethod
    def get_all():
        """
        取得所有收支記錄。
        :return: list of sqlite3.Row，所有收支明細，預設依日期與 ID 降冪排序
        """
        query = 'SELECT * FROM transactions ORDER BY date DESC, id DESC'
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(query)
            return cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f"讀取所有記錄失敗: {e}")
            raise
        finally:
            if conn:
                conn.close()

    @staticmethod
    def get_by_id(tx_id):
        """
        取得單筆收支記錄。
        :param tx_id: int，記錄的 ID
        :return: sqlite3.Row 或 None
        """
        query = 'SELECT * FROM transactions WHERE id = ?'
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(query, (tx_id,))
            return cursor.fetchone()
        except sqlite3.Error as e:
            logger.error(f"讀取單筆記錄 (ID: {tx_id}) 失敗: {e}")
            raise
        finally:
            if conn:
                conn.close()

    @staticmethod
    def update(tx_id, data):
        """
        更新特定記錄。
        :param tx_id: int，記錄的 ID
        :param data: dict，包含更新後的 'type', 'amount', 'category', 'date', 'note'
        :return: bool，是否更新成功
        """
        query = '''
            UPDATE transactions
            SET type = ?, amount = ?, category = ?, date = ?, note = ?
            WHERE id = ?
        '''
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(query, (
                data.get('type'),
                data.get('amount'),
                data.get('category'),
                data.get('date'),
                data.get('note', ''),
                tx_id
            ))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            logger.error(f"更新記錄 (ID: {tx_id}) 失敗: {e}")
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                conn.close()

    @staticmethod
    def delete(tx_id):
        """
        刪除特定記錄。
        :param tx_id: int，記錄的 ID
        :return: bool，是否刪除成功
        """
        query = 'DELETE FROM transactions WHERE id = ?'
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(query, (tx_id,))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            logger.error(f"刪除記錄 (ID: {tx_id}) 失敗: {e}")
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                conn.close()
