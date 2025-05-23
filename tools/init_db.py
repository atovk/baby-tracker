#!/usr/bin/env python
"""
数据库初始化脚本 - 使用 Alembic 初始化数据库并填充初始数据
"""
import os
import sys
import argparse
import subprocess
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from baby_tracker.database import engine, get_db
from baby_tracker.models.lookup import DiaperDesc, SleepDesc, FeedDesc


def run_alembic_migration(db_path=None):
    """运行数据库迁移"""
    print("开始运行 Alembic 数据库迁移...")
    
    # 如果指定了数据库路径，更新 alembic.ini 中的 URL
    if db_path:
        # 直接修改配置文件而不使用ConfigParser来避免重复选项问题
        alembic_ini = os.path.join(project_root, 'alembic.ini')
        with open(alembic_ini, 'r') as f:
            config_lines = f.readlines()
        
        # 构建 SQLite URL
        db_url = f"sqlite:///{db_path}"
        
        # 构建 SQLite URL
        db_url = f"sqlite:///{db_path}"
        config['alembic']['sqlalchemy.url'] = db_url
        
        # 写回配置文件
        with open(alembic_ini, 'w') as f:
            config.write(f)
        
        print(f"已更新数据库连接 URL 为: {db_url}")
    
    # 运行 Alembic 迁移
    try:
        alembic_path = os.path.join(project_root, 'alembic')
        result = subprocess.run(
            ['alembic', 'upgrade', 'head'],
            cwd=project_root,
            check=True,
            capture_output=True,
            text=True
        )
        print("Alembic 迁移成功:")
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Alembic 迁移失败: {e}")
        print(e.stdout)
        print(e.stderr)
        return False


def populate_lookup_tables():
    """填充查找表数据"""
    print("开始填充查找表数据...")
    db = next(get_db())
    
    try:
        # 尿布类型描述
        diaper_types = [
            DiaperDesc(id="1", name="尿尿", description="只有尿液"),
            DiaperDesc(id="2", name="便便", description="只有大便"),
            DiaperDesc(id="3", name="混合", description="尿液和大便"),
            DiaperDesc(id="4", name="干燥", description="尿布干燥，只是例行更换")
        ]
        
        # 睡眠描述
        sleep_types = [
            SleepDesc(id="1", name="小睡", description="短时间休息，通常不超过30分钟"),
            SleepDesc(id="2", name="午睡", description="白天的较长睡眠"),
            SleepDesc(id="3", name="夜间睡眠", description="晚上的主要睡眠时段")
        ]
        
        # 喂养描述
        feed_types = [
            FeedDesc(id="1", name="常规喂养", description="正常的日常喂养", category="nursing"),
            FeedDesc(id="2", name="做梦吃奶", description="宝宝在睡梦中吃奶", category="nursing"),
            FeedDesc(id="3", name="安抚吃奶", description="用于安抚宝宝情绪的吃奶", category="nursing"),
            FeedDesc(id="4", name="常规奶粉", description="标准配方的奶粉", category="formula"),
            FeedDesc(id="5", name="特殊配方", description="特殊配方的奶粉，如抗过敏", category="formula"),
            FeedDesc(id="6", name="果泥", description="水果泥", category="solids"),
            FeedDesc(id="7", name="蔬菜泥", description="蔬菜泥", category="solids"),
            FeedDesc(id="8", name="谷物", description="谷物类辅食", category="solids")
        ]
        
        # 添加到数据库
        for desc in diaper_types:
            db.merge(desc)
        
        for desc in sleep_types:
            db.merge(desc)
        
        for desc in feed_types:
            db.merge(desc)
        
        db.commit()
        print("查找表数据填充成功")
        return True
    
    except Exception as e:
        print(f"填充查找表数据时出错: {e}")
        db.rollback()
        return False
    finally:
        db.close()


def create_data_directory(data_dir):
    """创建数据目录"""
    try:
        os.makedirs(data_dir, exist_ok=True)
        print(f"已创建数据目录: {data_dir}")
        return True
    except Exception as e:
        print(f"创建数据目录时出错: {e}")
        return False


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="宝宝追踪器数据库初始化工具")
    parser.add_argument("--db-path", type=str, default="data/baby_tracker.db", help="数据库文件路径")
    parser.add_argument("--skip-migration", action="store_true", help="跳过数据库迁移")
    parser.add_argument("--skip-lookup", action="store_true", help="跳过查找表数据填充")
    args = parser.parse_args()
    
    # 确保数据目录存在
    data_dir = os.path.dirname(args.db_path)
    if data_dir and not os.path.exists(data_dir):
        if not create_data_directory(data_dir):
            return 1
    
    # 运行数据库迁移
    if not args.skip_migration:
        if not run_alembic_migration(args.db_path):
            return 1
    
    # 填充查找表数据
    if not args.skip_lookup:
        if not populate_lookup_tables():
            return 1
    
    print("数据库初始化完成！")
    return 0


if __name__ == "__main__":
    sys.exit(main())
