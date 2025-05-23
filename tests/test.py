# 加载 sqlite db文件
import sqlite3
import os
import pandas as pd


def load_sqlite_db(db_path):
    # 检查文件是否存在
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database file {db_path} does not exist.")
    
    # 连接到 SQLite 数据库
    conn = sqlite3.connect(db_path)
    
    # 获取所有表名
    query = "SELECT name FROM sqlite_master WHERE type='table';"
    tables = pd.read_sql_query(query, conn)
    
    # 读取每个表的数据
    dataframes = {}
    for table in tables['name']:
        df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
        dataframes[table] = df
    
    # 关闭连接
    conn.close()
    
    return dataframes


# 测试函数
if __name__ == "__main__":
    db_path = './EasyLog.db'  # 替换为你的数据库文件路径
    try:
        dataframes = load_sqlite_db(db_path)
        for table_name, df in dataframes.items():
            print(f"Table: {table_name}")
            print(df.head())  # 打印每个表的前5行数据
    except Exception as e:
        print(f"Error: {e}")