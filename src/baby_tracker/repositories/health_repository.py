"""
健康相关仓储 - 使用 dataclasses DTO
"""
from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy import func, and_
from sqlalchemy.orm import Session
from baby_tracker.models.dto import (
    SleepDTO, DiaperDTO, WeightDTO, HeightDTO, HeadDTO, TemperatureDTO
)
from baby_tracker.models.mappers import (
    SleepMapper, DiaperMapper, WeightMapper, HeightMapper, HeadMapper, TemperatureMapper
)
from baby_tracker.repositories.base_repository import BaseRepository


class SleepRepository(BaseRepository[SleepDTO, 'Sleep']):
    """睡眠记录仓储"""
    
    def _get_model_class(self):
        from baby_tracker.models.health import Sleep
        return Sleep
    
    def _get_mapper(self):
        return SleepMapper
    
    def find_by_baby_id(self, baby_id: str, limit: Optional[int] = None) -> List[SleepDTO]:
        """根据宝宝ID查找睡眠记录"""
        query = self.db_session.query(self.model_class).filter(
            self.model_class.baby_id == baby_id
        ).order_by(self.model_class.time.desc())
        
        if limit:
            query = query.limit(limit)
        
        model_instances = query.all()
        return [self.mapper.to_dto(instance) for instance in model_instances]
    
    def find_by_date_range(self, baby_id: str, start_date: datetime, end_date: datetime) -> List[SleepDTO]:
        """根据日期范围查找睡眠记录"""
        start_timestamp = start_date.timestamp()
        end_timestamp = end_date.timestamp()
        
        model_instances = self.db_session.query(self.model_class).filter(
            and_(
                self.model_class.baby_id == baby_id,
                self.model_class.time.between(start_timestamp, end_timestamp)
            )
        ).order_by(self.model_class.time.desc()).all()
        
        return [self.mapper.to_dto(instance) for instance in model_instances]
    
    def get_daily_sleep_duration(self, baby_id: str, date: datetime) -> int:
        """获取指定日期的睡眠总时长（分钟）"""
        start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)
        
        start_timestamp = start_of_day.timestamp()
        end_timestamp = end_of_day.timestamp()
        
        result = self.db_session.query(func.sum(self.model_class.duration)).filter(
            and_(
                self.model_class.baby_id == baby_id,
                self.model_class.time.between(start_timestamp, end_timestamp)
            )
        ).scalar()
        
        return result or 0
    
    def get_weekly_average_sleep(self, baby_id: str, end_date: datetime) -> float:
        """获取一周内的平均睡眠时长（小时）"""
        start_date = end_date - timedelta(days=7)
        start_timestamp = start_date.timestamp()
        end_timestamp = end_date.timestamp()
        
        result = self.db_session.query(
            func.avg(func.sum(self.model_class.duration))
        ).filter(
            and_(
                self.model_class.baby_id == baby_id,
                self.model_class.time.between(start_timestamp, end_timestamp)
            )
        ).group_by(
            func.strftime("%Y-%m-%d", func.datetime(self.model_class.time, 'unixepoch'))
        ).scalar()
        
        return (result or 0) / 60  # 转换为小时


class DiaperRepository(BaseRepository[DiaperDTO, 'Diaper']):
    """尿布记录仓储"""
    
    def _get_model_class(self):
        from baby_tracker.models.health import Diaper
        return Diaper
    
    def _get_mapper(self):
        return DiaperMapper
    
    def find_by_baby_id(self, baby_id: str, limit: Optional[int] = None) -> List[DiaperDTO]:
        """根据宝宝ID查找尿布记录"""
        query = self.db_session.query(self.model_class).filter(
            self.model_class.baby_id == baby_id
        ).order_by(self.model_class.time.desc())
        
        if limit:
            query = query.limit(limit)
        
        model_instances = query.all()
        return [self.mapper.to_dto(instance) for instance in model_instances]
    
    def find_by_date_range(self, baby_id: str, start_date: datetime, end_date: datetime) -> List[DiaperDTO]:
        """根据日期范围查找尿布记录"""
        start_timestamp = start_date.timestamp()
        end_timestamp = end_date.timestamp()
        
        model_instances = self.db_session.query(self.model_class).filter(
            and_(
                self.model_class.baby_id == baby_id,
                self.model_class.time.between(start_timestamp, end_timestamp)
            )
        ).order_by(self.model_class.time.desc()).all()
        
        return [self.mapper.to_dto(instance) for instance in model_instances]
    
    def get_daily_diaper_count(self, baby_id: str, date: datetime) -> int:
        """获取指定日期的尿布更换次数"""
        start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)
        
        start_timestamp = start_of_day.timestamp()
        end_timestamp = end_of_day.timestamp()
        
        return self.db_session.query(self.model_class).filter(
            and_(
                self.model_class.baby_id == baby_id,
                self.model_class.time.between(start_timestamp, end_timestamp)
            )
        ).count()


class WeightRepository(BaseRepository[WeightDTO, 'Weight']):
    """体重记录仓储"""
    
    def _get_model_class(self):
        from baby_tracker.models.health import Weight
        return Weight
    
    def _get_mapper(self):
        return WeightMapper
    
    def find_by_baby_id(self, baby_id: str, limit: Optional[int] = None) -> List[WeightDTO]:
        """根据宝宝ID查找体重记录"""
        query = self.db_session.query(self.model_class).filter(
            self.model_class.baby_id == baby_id
        ).order_by(self.model_class.time.desc())
        
        if limit:
            query = query.limit(limit)
        
        model_instances = query.all()
        return [self.mapper.to_dto(instance) for instance in model_instances]
    
    def get_latest_weight(self, baby_id: str) -> Optional[WeightDTO]:
        """获取最新的体重记录"""
        model_instance = self.db_session.query(self.model_class).filter(
            self.model_class.baby_id == baby_id
        ).order_by(self.model_class.time.desc()).first()
        
        return self.mapper.to_dto(model_instance) if model_instance else None
    
    def calculate_weight_gain(self, baby_id: str, days: int = 30) -> float:
        """计算过去指定天数的体重增长（克）"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        start_timestamp = start_date.timestamp()
        end_timestamp = end_date.timestamp()
        
        # 获取时间范围内的所有记录
        records = self.db_session.query(self.model_class).filter(
            and_(
                self.model_class.baby_id == baby_id,
                self.model_class.time.between(start_timestamp, end_timestamp)
            )
        ).order_by(self.model_class.time.asc()).all()
        
        if len(records) < 2:
            return 0
        
        # 计算体重增长
        first = records[0]
        last = records[-1]
        
        return last.weight - first.weight


class HeightRepository(BaseRepository[HeightDTO, 'Height']):
    """身高记录仓储"""
    
    def _get_model_class(self):
        from baby_tracker.models.health import Height
        return Height
    
    def _get_mapper(self):
        return HeightMapper
    
    def find_by_baby_id(self, baby_id: str, limit: Optional[int] = None) -> List[HeightDTO]:
        """根据宝宝ID查找身高记录"""
        query = self.db_session.query(self.model_class).filter(
            self.model_class.baby_id == baby_id
        ).order_by(self.model_class.time.desc())
        
        if limit:
            query = query.limit(limit)
        
        model_instances = query.all()
        return [self.mapper.to_dto(instance) for instance in model_instances]
    
    def get_latest_height(self, baby_id: str) -> Optional[HeightDTO]:
        """获取最新的身高记录"""
        model_instance = self.db_session.query(self.model_class).filter(
            self.model_class.baby_id == baby_id
        ).order_by(self.model_class.time.desc()).first()
        
        return self.mapper.to_dto(model_instance) if model_instance else None


class HeadRepository(BaseRepository[HeadDTO, 'Head']):
    """头围记录仓储"""
    
    def _get_model_class(self):
        from baby_tracker.models.health import Head
        return Head
    
    def _get_mapper(self):
        return HeadMapper
    
    def find_by_baby_id(self, baby_id: str, limit: Optional[int] = None) -> List[HeadDTO]:
        """根据宝宝ID查找头围记录"""
        query = self.db_session.query(self.model_class).filter(
            self.model_class.baby_id == baby_id
        ).order_by(self.model_class.time.desc())
        
        if limit:
            query = query.limit(limit)
        
        model_instances = query.all()
        return [self.mapper.to_dto(instance) for instance in model_instances]
    
    def get_latest_head(self, baby_id: str) -> Optional[HeadDTO]:
        """获取最新的头围记录"""
        model_instance = self.db_session.query(self.model_class).filter(
            self.model_class.baby_id == baby_id
        ).order_by(self.model_class.time.desc()).first()
        
        return self.mapper.to_dto(model_instance) if model_instance else None


class TemperatureRepository(BaseRepository[TemperatureDTO, 'Temperature']):
    """体温记录仓储"""
    
    def _get_model_class(self):
        from baby_tracker.models.health import Temperature
        return Temperature
    
    def _get_mapper(self):
        return TemperatureMapper
    
    def find_by_baby_id(self, baby_id: str, limit: Optional[int] = None) -> List[TemperatureDTO]:
        """根据宝宝ID查找体温记录"""
        query = self.db_session.query(self.model_class).filter(
            self.model_class.baby_id == baby_id
        ).order_by(self.model_class.time.desc())
        
        if limit:
            query = query.limit(limit)
        
        model_instances = query.all()
        return [self.mapper.to_dto(instance) for instance in model_instances]
    
    def find_fever_records(self, baby_id: str, days: int = 30) -> List[TemperatureDTO]:
        """查找指定天数内的发烧记录"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        start_timestamp = start_date.timestamp()
        end_timestamp = end_date.timestamp()
        
        model_instances = self.db_session.query(self.model_class).filter(
            and_(
                self.model_class.baby_id == baby_id,
                self.model_class.time.between(start_timestamp, end_timestamp),
                self.model_class.temperature >= 37.5
            )
        ).order_by(self.model_class.time.desc()).all()
        
        return [self.mapper.to_dto(instance) for instance in model_instances]
