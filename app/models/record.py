import sqlite3
import os
import logging

# 預設將資料庫存在 instance/database.db，符合系統架構文件
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'database.db')

def get_db_connection():
    """
    建立 sqlite3 資料庫連線並回傳 connection。
    使用 row_factory = sqlite3.Row 讓查詢結果可以用欄位名稱取值。
    """
    try:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        logging.error(f"Database connection failed: {e}")
        raise

class RecordModel:
    @staticmethod
    def init_db():
        """
        初始化資料庫與資料表。
        讀取 database/schema.sql 來建立所需的資料表。
        """
        try:
            schema_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'database', 'schema.sql')
            if os.path.exists(schema_path):
                with open(schema_path, 'r', encoding='utf-8') as f:
                    schema_script = f.read()
                conn = get_db_connection()
                conn.executescript(schema_script)
                conn.commit()
                conn.close()
        except Exception as e:
            logging.error(f"Error initializing database: {e}")
            raise

    @staticmethod
    def create(data):
        """
        新增一筆記錄
        :param data: dict 包含 type, amount, category, date, description 等欄位資料
        :return: new_id (新增資料的主鍵識別碼)
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO records (type, amount, category, date, description)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                data.get('type'), 
                data.get('amount'), 
                data.get('category'), 
                data.get('date'), 
                data.get('description', '')
            ))
            conn.commit()
            new_id = cursor.lastrowid
            conn.close()
            return new_id
        except Exception as e:
            logging.error(f"Error creating record: {e}")
            raise

    @staticmethod
    def get_all():
        """
        取得所有記錄
        :return: list of dict representing all records (sorted by date descending)
        """
        try:
            conn = get_db_connection()
            records = conn.execute('SELECT * FROM records ORDER BY date DESC, id DESC').fetchall()
            conn.close()
            return [dict(row) for row in records]
        except Exception as e:
            logging.error(f"Error fetching all records: {e}")
            raise

    @staticmethod
    def get_by_id(record_id):
        """
        取得單筆記錄
        :param record_id: int 紀錄的 ID
        :return: dict representing the single record, or None if not found
        """
        try:
            conn = get_db_connection()
            record = conn.execute('SELECT * FROM records WHERE id = ?', (record_id,)).fetchone()
            conn.close()
            return dict(record) if record else None
        except Exception as e:
            logging.error(f"Error fetching record {record_id}: {e}")
            raise

    @staticmethod
    def update(record_id, data):
        """
        更新記錄
        :param record_id: int 目標紀錄 ID
        :param data: dict 包含更新的欄位資料
        """
        try:
            conn = get_db_connection()
            conn.execute('''
                UPDATE records
                SET type = ?, amount = ?, category = ?, date = ?, description = ?
                WHERE id = ?
            ''', (
                data.get('type'), 
                data.get('amount'), 
                data.get('category'), 
                data.get('date'), 
                data.get('description', ''), 
                record_id
            ))
            conn.commit()
            conn.close()
        except Exception as e:
            logging.error(f"Error updating record {record_id}: {e}")
            raise

    @staticmethod
    def delete(record_id):
        """
        刪除記錄
        :param record_id: int 欲刪除的紀錄 ID
        """
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM records WHERE id = ?', (record_id,))
            conn.commit()
            conn.close()
        except Exception as e:
            logging.error(f"Error deleting record {record_id}: {e}")
            raise
