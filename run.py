#!/usr/bin/env python
"""
宝宝追踪器启动脚本 - 一键启动应用程序
"""
import sys
import os
import argparse
import logging
import subprocess
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def init_database(db_path, reset=False):
    """初始化数据库"""
    print(f"初始化数据库: {db_path}")
    
    # 如果需要重置，删除现有数据库文件
    if reset and os.path.exists(db_path):
        try:
            os.remove(db_path)
            print(f"已删除现有数据库文件: {db_path}")
        except Exception as e:
            print(f"删除数据库文件失败: {e}")
            return False
    
    # 运行数据库初始化脚本
    init_script = os.path.join(project_root, "tools", "init_db.py")
    try:
        result = subprocess.run(
            [sys.executable, init_script, f"--db-path={db_path}"],
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"数据库初始化失败: {e}")
        print(e.stdout)
        print(e.stderr)
        return False


def run_migration():
    """运行数据库迁移"""
    print("运行数据库迁移...")
    
    try:
        result = subprocess.run(
            ["alembic", "upgrade", "head"],
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"迁移失败: {e}")
        print(e.stdout)
        print(e.stderr)
        return False


def create_demo_data():
    """创建演示数据"""
    print("创建演示数据...")
    
    demo_script = os.path.join(project_root, "examples", "full_demo.py")
    try:
        result = subprocess.run(
            [sys.executable, demo_script],
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"创建演示数据失败: {e}")
        print(e.stdout)
        print(e.stderr)
        return False


def run_app():
    """启动应用程序"""
    print("启动宝宝追踪器应用程序...")
    
    try:
        from baby_tracker.tracker import run_tracker
        run_tracker()
        return True
    except Exception as e:
        print(f"启动应用程序失败: {e}")
        return False


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="宝宝追踪器启动工具")
    parser.add_argument("--db-path", type=str, default="data/baby_tracker.db", help="数据库文件路径")
    parser.add_argument("--reset-db", action="store_true", help="重置数据库")
    parser.add_argument("--init-only", action="store_true", help="只初始化数据库，不启动应用")
    parser.add_argument("--demo-data", action="store_true", help="创建演示数据")
    parser.add_argument("--debug", action="store_true", help="启用调试模式")
    args = parser.parse_args()
    
    # 配置日志级别
    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # 初始化数据库
    if args.reset_db or args.init_only:
        if not init_database(args.db_path, reset=args.reset_db):
            return 1
    
    # 创建演示数据
    if args.demo_data:
        if not create_demo_data():
            return 1
    
    # 如果只初始化，到此为止
    if args.init_only:
        print("数据库初始化完成")
        return 0
    
    # 启动应用程序
    if not run_app():
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
