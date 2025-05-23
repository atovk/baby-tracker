#!/usr/bin/env python
"""
简化版数据库迁移脚本 - 使用 Alembic 初始化数据库
"""
import os
import sys
import subprocess
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def run_alembic_migration():
    """运行数据库迁移"""
    print("开始运行 Alembic 数据库迁移...")
    
    # 运行 Alembic 迁移
    try:
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

if __name__ == "__main__":
    run_alembic_migration()
