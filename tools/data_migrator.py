#!/usr/bin/env python
"""
数据迁移工具 - 用于将旧数据库结构迁移到新的数据库结构
"""
import os
import sys
import sqlite3
import uuid
import logging
import argparse
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from baby_tracker.database import engine, get_db
from baby_tracker.models.dto import (
    BabyDTO, NursingDTO, FormulaDTO, SleepDTO, DiaperDTO,
    WeightDTO, HeightDTO, TemperatureDTO, Gender, FinishSide,
    PlaytimeDTO, BathDTO, PhotoDTO, VideoDTO
)
from baby_tracker.services import (
    BabyService, FeedingService, HealthService, ActivityService
)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("data_migration.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("data_migration")


class DataMigrator:
    """数据迁移工具类"""
    
    def __init__(self, old_db_path, new_db_url=None):
        """
        初始化迁移工具
        
        Args:
            old_db_path (str): 旧数据库文件路径
            new_db_url (str): 新数据库URL，如果为None则使用默认URL
        """
        self.old_db_path = old_db_path
        self.new_db_url = new_db_url or "sqlite:///data/baby_tracker_new.db"
        self.old_conn = None
        self.new_engine = None
        self.session = None
        self.baby_service = None
        self.feeding_service = None
        self.health_service = None
        self.activity_service = None
        
        # 统计信息
        self.stats = {
            'baby': {'total': 0, 'migrated': 0, 'failed': 0},
            'nursing': {'total': 0, 'migrated': 0, 'failed': 0},
            'formula': {'total': 0, 'migrated': 0, 'failed': 0},
            'sleep': {'total': 0, 'migrated': 0, 'failed': 0},
            'diaper': {'total': 0, 'migrated': 0, 'failed': 0},
            'weight': {'total': 0, 'migrated': 0, 'failed': 0},
            'height': {'total': 0, 'migrated': 0, 'failed': 0},
            'temperature': {'total': 0, 'migrated': 0, 'failed': 0},
            'playtime': {'total': 0, 'migrated': 0, 'failed': 0},
            'bath': {'total': 0, 'migrated': 0, 'failed': 0},
            'photo': {'total': 0, 'migrated': 0, 'failed': 0},
            'video': {'total': 0, 'migrated': 0, 'failed': 0}
        }
    
    def connect(self):
        """连接到数据库"""
        try:
            logger.info(f"连接到旧数据库: {self.old_db_path}")
            self.old_conn = sqlite3.connect(self.old_db_path)
            self.old_conn.row_factory = sqlite3.Row
            
            logger.info(f"连接到新数据库: {self.new_db_url}")
            self.new_engine = create_engine(self.new_db_url)
            Session = sessionmaker(bind=self.new_engine)
            self.session = Session()
            
            # 初始化服务
            self.baby_service = BabyService(self.session)
            self.feeding_service = FeedingService(self.session)
            self.health_service = HealthService(self.session)
            self.activity_service = ActivityService(self.session)
            
            return True
        except Exception as e:
            logger.error(f"连接数据库失败: {e}")
            return False
    
    def migrate_babies(self):
        """迁移宝宝数据"""
        logger.info("开始迁移宝宝数据...")
        cursor = self.old_conn.cursor()
        cursor.execute("SELECT * FROM Baby")
        rows = cursor.fetchall()
        self.stats['baby']['total'] = len(rows)
        
        for row in rows:
            try:
                baby_dto = BabyDTO(
                    id=row['ID'],
                    name=row['Name'],
                    dob=row['DOB'],
                    due_day=row.get('DueDay'),
                    gender=Gender(row.get('Gender', 0)),
                    picture=row.get('Picture'),
                    timestamp=row.get('Timestamp', datetime.now().timestamp())
                )
                self.baby_service.create_baby(baby_dto)
                logger.info(f"迁移宝宝数据成功: {baby_dto.name} (ID: {baby_dto.id})")
                self.stats['baby']['migrated'] += 1
            except Exception as e:
                logger.error(f"迁移宝宝数据失败: {row['ID']} - {e}")
                self.stats['baby']['failed'] += 1
        
        logger.info(f"宝宝数据迁移完成: {self.stats['baby']['migrated']}/{self.stats['baby']['total']} 成功")
    
    def migrate_nursing(self):
        """迁移母乳喂养数据"""
        logger.info("开始迁移母乳喂养数据...")
        cursor = self.old_conn.cursor()
        cursor.execute("SELECT * FROM Nursing")
        rows = cursor.fetchall()
        self.stats['nursing']['total'] = len(rows)
        
        for row in rows:
            try:
                nursing_dto = NursingDTO(
                    id=row['ID'],
                    baby_id=row['BabyID'],
                    time=row['Time'],
                    note=row.get('Note'),
                    has_picture=bool(row.get('HasPicture', 0)),
                    desc_id=row.get('DescID'),
                    finish_side=FinishSide(row.get('FinishSide', 2)),
                    left_duration=row.get('LeftDuration', 0),
                    right_duration=row.get('RightDuration', 0),
                    both_duration=row.get('BothDuration', 0),
                    timestamp=row.get('Timestamp', datetime.now().timestamp())
                )
                self.feeding_service.nursing_repo.create(nursing_dto)
                logger.info(f"迁移母乳喂养数据成功: ID: {nursing_dto.id}")
                self.stats['nursing']['migrated'] += 1
            except Exception as e:
                logger.error(f"迁移母乳喂养数据失败: {row['ID']} - {e}")
                self.stats['nursing']['failed'] += 1
        
        logger.info(f"母乳喂养数据迁移完成: {self.stats['nursing']['migrated']}/{self.stats['nursing']['total']} 成功")
    
    def migrate_formula(self):
        """迁移配方奶数据"""
        logger.info("开始迁移配方奶数据...")
        cursor = self.old_conn.cursor()
        cursor.execute("SELECT * FROM Formula")
        rows = cursor.fetchall()
        self.stats['formula']['total'] = len(rows)
        
        for row in rows:
            try:
                formula_dto = FormulaDTO(
                    id=row['ID'],
                    baby_id=row['BabyID'],
                    time=row['Time'],
                    note=row.get('Note'),
                    has_picture=bool(row.get('HasPicture', 0)),
                    desc_id=row.get('DescID'),
                    amount=row.get('Amount', 0.0),
                    timestamp=row.get('Timestamp', datetime.now().timestamp())
                )
                self.feeding_service.formula_repo.create(formula_dto)
                logger.info(f"迁移配方奶数据成功: ID: {formula_dto.id}")
                self.stats['formula']['migrated'] += 1
            except Exception as e:
                logger.error(f"迁移配方奶数据失败: {row['ID']} - {e}")
                self.stats['formula']['failed'] += 1
        
        logger.info(f"配方奶数据迁移完成: {self.stats['formula']['migrated']}/{self.stats['formula']['total']} 成功")
    
    def migrate_sleep(self):
        """迁移睡眠数据"""
        logger.info("开始迁移睡眠数据...")
        cursor = self.old_conn.cursor()
        cursor.execute("SELECT * FROM Sleep")
        rows = cursor.fetchall()
        self.stats['sleep']['total'] = len(rows)
        
        for row in rows:
            try:
                sleep_dto = SleepDTO(
                    id=row['ID'],
                    baby_id=row['BabyID'],
                    time=row['Time'],
                    note=row.get('Note'),
                    has_picture=bool(row.get('HasPicture', 0)),
                    desc_id=row.get('DescID'),
                    duration=row.get('Duration', 0),
                    timestamp=row.get('Timestamp', datetime.now().timestamp())
                )
                self.health_service.sleep_repo.create(sleep_dto)
                logger.info(f"迁移睡眠数据成功: ID: {sleep_dto.id}")
                self.stats['sleep']['migrated'] += 1
            except Exception as e:
                logger.error(f"迁移睡眠数据失败: {row['ID']} - {e}")
                self.stats['sleep']['failed'] += 1
        
        logger.info(f"睡眠数据迁移完成: {self.stats['sleep']['migrated']}/{self.stats['sleep']['total']} 成功")
    
    def migrate_diaper(self):
        """迁移尿布数据"""
        logger.info("开始迁移尿布数据...")
        cursor = self.old_conn.cursor()
        cursor.execute("SELECT * FROM Diaper")
        rows = cursor.fetchall()
        self.stats['diaper']['total'] = len(rows)
        
        for row in rows:
            try:
                diaper_dto = DiaperDTO(
                    id=row['ID'],
                    baby_id=row['BabyID'],
                    time=row['Time'],
                    note=row.get('Note'),
                    has_picture=bool(row.get('HasPicture', 0)),
                    desc_id=row.get('DescID'),
                    timestamp=row.get('Timestamp', datetime.now().timestamp())
                )
                self.health_service.diaper_repo.create(diaper_dto)
                logger.info(f"迁移尿布数据成功: ID: {diaper_dto.id}")
                self.stats['diaper']['migrated'] += 1
            except Exception as e:
                logger.error(f"迁移尿布数据失败: {row['ID']} - {e}")
                self.stats['diaper']['failed'] += 1
        
        logger.info(f"尿布数据迁移完成: {self.stats['diaper']['migrated']}/{self.stats['diaper']['total']} 成功")
    
    def migrate_weight(self):
        """迁移体重数据"""
        logger.info("开始迁移体重数据...")
        cursor = self.old_conn.cursor()
        cursor.execute("SELECT * FROM Weight")
        rows = cursor.fetchall()
        self.stats['weight']['total'] = len(rows)
        
        for row in rows:
            try:
                weight_dto = WeightDTO(
                    id=row['ID'],
                    baby_id=row['BabyID'],
                    time=row['Time'],
                    note=row.get('Note'),
                    has_picture=bool(row.get('HasPicture', 0)),
                    weight=row['Weight'],
                    timestamp=row.get('Timestamp', datetime.now().timestamp())
                )
                self.health_service.weight_repo.create(weight_dto)
                logger.info(f"迁移体重数据成功: ID: {weight_dto.id}")
                self.stats['weight']['migrated'] += 1
            except Exception as e:
                logger.error(f"迁移体重数据失败: {row['ID']} - {e}")
                self.stats['weight']['failed'] += 1
        
        logger.info(f"体重数据迁移完成: {self.stats['weight']['migrated']}/{self.stats['weight']['total']} 成功")
    
    def migrate_height(self):
        """迁移身高数据"""
        logger.info("开始迁移身高数据...")
        cursor = self.old_conn.cursor()
        cursor.execute("SELECT * FROM Height")
        rows = cursor.fetchall()
        self.stats['height']['total'] = len(rows)
        
        for row in rows:
            try:
                height_dto = HeightDTO(
                    id=row['ID'],
                    baby_id=row['BabyID'],
                    time=row['Time'],
                    note=row.get('Note'),
                    has_picture=bool(row.get('HasPicture', 0)),
                    height=row['Height'],
                    timestamp=row.get('Timestamp', datetime.now().timestamp())
                )
                self.health_service.height_repo.create(height_dto)
                logger.info(f"迁移身高数据成功: ID: {height_dto.id}")
                self.stats['height']['migrated'] += 1
            except Exception as e:
                logger.error(f"迁移身高数据失败: {row['ID']} - {e}")
                self.stats['height']['failed'] += 1
        
        logger.info(f"身高数据迁移完成: {self.stats['height']['migrated']}/{self.stats['height']['total']} 成功")
    
    def migrate_head(self):
        """迁移头围数据"""
        logger.info("开始迁移头围数据...")
        cursor = self.old_conn.cursor()
        cursor.execute("SELECT * FROM Head")
        rows = cursor.fetchall()
        self.stats['head']['total'] = len(rows)
        
        for row in rows:
            try:
                head_dto = HeadDTO(
                    id=row['ID'],
                    baby_id=row['BabyID'],
                    time=row['Time'],
                    note=row.get('Note'),
                    has_picture=bool(row.get('HasPicture', 0)),
                    head=row['Head'],
                    timestamp=row.get('Timestamp', datetime.now().timestamp())
                )
                self.health_service.head_repo.create(head_dto)
                logger.info(f"迁移头围数据成功: ID: {head_dto.id}")
                self.stats['head']['migrated'] += 1
            except Exception as e:
                logger.error(f"迁移头围数据失败: {row['ID']} - {e}")
                self.stats['head']['failed'] += 1
        
        logger.info(f"头围数据迁移完成: {self.stats['head']['migrated']}/{self.stats['head']['total']} 成功")
    
    def migrate_temperature(self):
        """迁移体温数据"""
        logger.info("开始迁移体温数据...")
        cursor = self.old_conn.cursor()
        cursor.execute("SELECT * FROM Temperature")
        rows = cursor.fetchall()
        self.stats['temperature']['total'] = len(rows)
        
        for row in rows:
            try:
                temp_dto = TemperatureDTO(
                    id=row['ID'],
                    baby_id=row['BabyID'],
                    time=row['Time'],
                    note=row.get('Note'),
                    has_picture=bool(row.get('HasPicture', 0)),
                    temperature=row['Temperature'],
                    location=row.get('Location'),
                    timestamp=row.get('Timestamp', datetime.now().timestamp())
                )
                self.health_service.temp_repo.create(temp_dto)
                logger.info(f"迁移体温数据成功: ID: {temp_dto.id}")
                self.stats['temperature']['migrated'] += 1
            except Exception as e:
                logger.error(f"迁移体温数据失败: {row['ID']} - {e}")
                self.stats['temperature']['failed'] += 1
        
        logger.info(f"体温数据迁移完成: {self.stats['temperature']['migrated']}/{self.stats['temperature']['total']} 成功")
    
    def migrate_playtime(self):
        """迁移游戏时间数据"""
        logger.info("开始迁移游戏时间数据...")
        cursor = self.old_conn.cursor()
        cursor.execute("SELECT * FROM Playtime")
        rows = cursor.fetchall()
        self.stats['playtime']['total'] = len(rows)
        
        for row in rows:
            try:
                playtime_dto = PlaytimeDTO(
                    id=row['ID'],
                    baby_id=row['BabyID'],
                    time=row['Time'],
                    note=row.get('Note'),
                    has_picture=bool(row.get('HasPicture', 0)),
                    duration=row.get('Duration', 0),
                    play_type=row.get('PlayType'),
                    timestamp=row.get('Timestamp', datetime.now().timestamp())
                )
                self.activity_service.playtime_repo.create(playtime_dto)
                logger.info(f"迁移游戏时间数据成功: ID: {playtime_dto.id}")
                self.stats['playtime']['migrated'] += 1
            except Exception as e:
                logger.error(f"迁移游戏时间数据失败: {row['ID']} - {e}")
                self.stats['playtime']['failed'] += 1
        
        logger.info(f"游戏时间数据迁移完成: {self.stats['playtime']['migrated']}/{self.stats['playtime']['total']} 成功")
    
    def migrate_bath(self):
        """迁移洗澡数据"""
        logger.info("开始迁移洗澡数据...")
        cursor = self.old_conn.cursor()
        cursor.execute("SELECT * FROM Bath")
        rows = cursor.fetchall()
        self.stats['bath']['total'] = len(rows)
        
        for row in rows:
            try:
                bath_dto = BathDTO(
                    id=row['ID'],
                    baby_id=row['BabyID'],
                    time=row['Time'],
                    note=row.get('Note'),
                    has_picture=bool(row.get('HasPicture', 0)),
                    duration=row.get('Duration', 0),
                    water_temperature=row.get('WaterTemperature'),
                    timestamp=row.get('Timestamp', datetime.now().timestamp())
                )
                self.activity_service.bath_repo.create(bath_dto)
                logger.info(f"迁移洗澡数据成功: ID: {bath_dto.id}")
                self.stats['bath']['migrated'] += 1
            except Exception as e:
                logger.error(f"迁移洗澡数据失败: {row['ID']} - {e}")
                self.stats['bath']['failed'] += 1
        
        logger.info(f"洗澡数据迁移完成: {self.stats['bath']['migrated']}/{self.stats['bath']['total']} 成功")
    
    def migrate_photo(self):
        """迁移照片数据"""
        logger.info("开始迁移照片数据...")
        cursor = self.old_conn.cursor()
        cursor.execute("SELECT * FROM Photo")
        rows = cursor.fetchall()
        self.stats['photo']['total'] = len(rows)
        
        for row in rows:
            try:
                photo_dto = PhotoDTO(
                    id=row['ID'],
                    baby_id=row['BabyID'],
                    time=row['Time'],
                    note=row.get('Note'),
                    has_picture=bool(row.get('HasPicture', 0)),
                    file_path=row['FilePath'],
                    description=row.get('Description'),
                    timestamp=row.get('Timestamp', datetime.now().timestamp())
                )
                self.activity_service.photo_repo.create(photo_dto)
                logger.info(f"迁移照片数据成功: ID: {photo_dto.id}")
                self.stats['photo']['migrated'] += 1
            except Exception as e:
                logger.error(f"迁移照片数据失败: {row['ID']} - {e}")
                self.stats['photo']['failed'] += 1
        
        logger.info(f"照片数据迁移完成: {self.stats['photo']['migrated']}/{self.stats['photo']['total']} 成功")
    
    def migrate_video(self):
        """迁移视频数据"""
        logger.info("开始迁移视频数据...")
        cursor = self.old_conn.cursor()
        cursor.execute("SELECT * FROM Video")
        rows = cursor.fetchall()
        self.stats['video']['total'] = len(rows)
        
        for row in rows:
            try:
                video_dto = VideoDTO(
                    id=row['ID'],
                    baby_id=row['BabyID'],
                    time=row['Time'],
                    note=row.get('Note'),
                    has_picture=bool(row.get('HasPicture', 0)),
                    file_path=row['FilePath'],
                    duration=row.get('Duration', 0),
                    description=row.get('Description'),
                    timestamp=row.get('Timestamp', datetime.now().timestamp())
                )
                self.activity_service.video_repo.create(video_dto)
                logger.info(f"迁移视频数据成功: ID: {video_dto.id}")
                self.stats['video']['migrated'] += 1
            except Exception as e:
                logger.error(f"迁移视频数据失败: {row['ID']} - {e}")
                self.stats['video']['failed'] += 1
        
        logger.info(f"视频数据迁移完成: {self.stats['video']['migrated']}/{self.stats['video']['total']} 成功")
    
    def migrate_lookup_tables(self):
        """迁移查找表数据"""
        logger.info("开始迁移查找表数据...")
        
        # 迁移尿布描述
        cursor = self.old_conn.cursor()
        cursor.execute("SELECT * FROM DiaperDesc")
        rows = cursor.fetchall()
        for row in rows:
            try:
                query = f"INSERT INTO DiaperDesc (ID, Name, DisplayOrder) VALUES ('{row['ID']}', '{row['Name']}', {row.get('DisplayOrder', 0)})"
                self.session.execute(query)
                logger.info(f"迁移尿布描述成功: {row['Name']}")
            except Exception as e:
                logger.error(f"迁移尿布描述失败: {row['ID']} - {e}")
        
        # 迁移喂养描述
        cursor.execute("SELECT * FROM NursingDesc")
        rows = cursor.fetchall()
        for row in rows:
            try:
                query = f"INSERT INTO NursingDesc (ID, Name, DisplayOrder) VALUES ('{row['ID']}', '{row['Name']}', {row.get('DisplayOrder', 0)})"
                self.session.execute(query)
                logger.info(f"迁移喂养描述成功: {row['Name']}")
            except Exception as e:
                logger.error(f"迁移喂养描述失败: {row['ID']} - {e}")
        
        # 迁移配方奶描述
        cursor.execute("SELECT * FROM FormulaDesc")
        rows = cursor.fetchall()
        for row in rows:
            try:
                query = f"INSERT INTO FormulaDesc (ID, Name, DisplayOrder) VALUES ('{row['ID']}', '{row['Name']}', {row.get('DisplayOrder', 0)})"
                self.session.execute(query)
                logger.info(f"迁移配方奶描述成功: {row['Name']}")
            except Exception as e:
                logger.error(f"迁移配方奶描述失败: {row['ID']} - {e}")
        
        # 迁移睡眠描述
        cursor.execute("SELECT * FROM SleepDesc")
        rows = cursor.fetchall()
        for row in rows:
            try:
                query = f"INSERT INTO SleepDesc (ID, Name, DisplayOrder) VALUES ('{row['ID']}', '{row['Name']}', {row.get('DisplayOrder', 0)})"
                self.session.execute(query)
                logger.info(f"迁移睡眠描述成功: {row['Name']}")
            except Exception as e:
                logger.error(f"迁移睡眠描述失败: {row['ID']} - {e}")
        
        self.session.commit()
        logger.info("查找表数据迁移完成")
    
    def migrate_all(self):
        """迁移所有数据"""
        if not self.connect():
            logger.error("连接数据库失败，无法进行迁移")
            return False
        
        try:
            # 先迁移查找表
            self.migrate_lookup_tables()
            
            # 再迁移宝宝数据
            self.migrate_babies()
            
            # 然后迁移其他数据
            self.migrate_nursing()
            self.migrate_formula()
            self.migrate_sleep()
            self.migrate_diaper()
            self.migrate_weight()
            self.migrate_height()
            self.migrate_head()
            self.migrate_temperature()
            self.migrate_playtime()
            self.migrate_bath()
            self.migrate_photo()
            self.migrate_video()
            
            # 提交事务
            self.session.commit()
            
            # 打印统计结果
            self.print_stats()
            
            logger.info("所有数据迁移完成")
            return True
        except Exception as e:
            logger.error(f"数据迁移过程中出错: {e}")
            self.session.rollback()
            return False
        finally:
            if self.old_conn:
                self.old_conn.close()
            if self.session:
                self.session.close()
    
    def print_stats(self):
        """打印统计结果"""
        logger.info("========== 数据迁移统计 ==========")
        for category, stats in self.stats.items():
            if stats['total'] > 0:
                success_rate = (stats['migrated'] / stats['total']) * 100
                logger.info(f"{category}: 总数 {stats['total']}, 成功 {stats['migrated']} ({success_rate:.2f}%), 失败 {stats['failed']}")
            else:
                logger.info(f"{category}: 无数据")
        logger.info("=================================")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="宝宝追踪器数据迁移工具")
    parser.add_argument("--old-db", type=str, default="data/EasyLog.db", help="旧数据库文件路径")
    parser.add_argument("--new-db", type=str, default="sqlite:///data/baby_tracker_new.db", help="新数据库URL")
    args = parser.parse_args()
    
    migrator = DataMigrator(args.old_db, args.new_db)
    success = migrator.migrate_all()
    
    if success:
        logger.info("数据迁移成功完成")
        sys.exit(0)
    else:
        logger.error("数据迁移失败")
        sys.exit(1)


if __name__ == "__main__":
    main()
