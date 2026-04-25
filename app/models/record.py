import sqlite3
import os

# 預設將資料庫存在 instance/database.db，符合系統架構文件
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'database.db')

def get_db_connection():
    """建立資料庫連線並回傳 connection"""
    # 確保資料夾存在
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    # 將查詢結果轉為字典形式，方便在 Jinja2 取用欄位名
    conn.row_factory = sqlite3.Row
    return conn

class RecordModel:
    @staticmethod
    def init_db():
        """初始化資料庫與資料表"""
        schema_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'database', 'schema.sql')
        if os.path.exists(schema_path):
            with open(schema_path, 'r', encoding='utf-8') as f:
                schema_script = f.read()
            conn = get_db_connection()
            conn.executescript(schema_script)
            conn.commit()
            conn.close()

    @staticmethod
    def create(type, amount, category, date, description=""):
        """新增一筆紀錄"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO records (type, amount, category, date, description)
            VALUES (?, ?, ?, ?, ?)
        ''', (type, amount, category, date, description))
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return new_id

    @staticmethod
    def get_all():
        """取得所有收支紀錄，依照日期降序排列"""
        conn = get_db_connection()
        records = conn.execute('SELECT * FROM records ORDER BY date DESC, id DESC').fetchall()
        conn.close()
        return [dict(row) for row in records]

    @staticmethod
    def get_by_id(record_id):
        """根據 ID 取得單一筆紀錄"""
        conn = get_db_connection()
        record = conn.execute('SELECT * FROM records WHERE id = ?', (record_id,)).fetchone()
        conn.close()
        return dict(record) if record else None

    @staticmethod
    def update(record_id, type, amount, category, date, description=""):
        """更新指定 ID 的紀錄"""
        conn = get_db_connection()
        conn.execute('''
            UPDATE records
            SET type = ?, amount = ?, category = ?, date = ?, description = ?
            WHERE id = ?
        ''', (type, amount, category, date, description, record_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(record_id):
        """刪除指定 ID 的紀錄"""
        conn = get_db_connection()
        conn.execute('DELETE FROM records WHERE id = ?', (record_id,))
        conn.commit()
        conn.close()
