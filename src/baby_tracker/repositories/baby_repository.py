"""
宝宝信息仓储 - 使用 dataclasses DTO
"""
from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from baby_tracker.models.dto import BabyDTO
from baby_tracker.models.mappers import BabyMapper
from baby_tracker.repositories.base_repository import BaseRepository


class BabyRepository(BaseRepository[BabyDTO, 'Baby']):
    """宝宝信息仓储"""
    
    def _get_model_class(self):
        from baby_tracker.models.baby import Baby
        return Baby
    
    def _get_mapper(self):
        return BabyMapper
    
    def find_by_name(self, name: str) -> List[BabyDTO]:
        """根据姓名查找宝宝"""
        model_instances = self.db_session.query(self.model_class).filter(
            self.model_class.name.ilike(f"%{name}%")
        ).all()
        return [self.mapper.to_dto(instance) for instance in model_instances]
    
    def find_by_gender(self, gender: int) -> List[BabyDTO]:
        """根据性别查找宝宝"""
        model_instances = self.db_session.query(self.model_class).filter(
            self.model_class.gender == gender
        ).all()
        return [self.mapper.to_dto(instance) for instance in model_instances]
    
    def find_babies_born_after(self, date: datetime) -> List[BabyDTO]:
        """查找指定日期后出生的宝宝"""
        timestamp = date.timestamp()
        model_instances = self.db_session.query(self.model_class).filter(
            self.model_class.dob >= timestamp
        ).all()
        return [self.mapper.to_dto(instance) for instance in model_instances]
    
    def find_babies_by_age_range(self, min_days: int, max_days: int) -> List[BabyDTO]:
        """根据年龄范围查找宝宝"""
        now = datetime.now()
        max_date = now - timedelta(days=min_days)
        min_date = now - timedelta(days=max_days)
        
        max_timestamp = max_date.timestamp()
        min_timestamp = min_date.timestamp()
        
        model_instances = self.db_session.query(self.model_class).filter(
            self.model_class.dob.between(min_timestamp, max_timestamp)
        ).all()
        return [self.mapper.to_dto(instance) for instance in model_instances]
    
    def get_babies_with_recent_activity(self, days: int = 7) -> List[BabyDTO]:
        """获取最近有活动的宝宝"""
        cutoff_date = datetime.now() - timedelta(days=days)
        cutoff_timestamp = cutoff_date.timestamp()
        
        # 这里可以扩展查询包含最近的喂养、睡眠等活动
        model_instances = self.db_session.query(self.model_class).filter(
            self.model_class.timestamp >= cutoff_timestamp
        ).all()
        return [self.mapper.to_dto(instance) for instance in model_instances]
