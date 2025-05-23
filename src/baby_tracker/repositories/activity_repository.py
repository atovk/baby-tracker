"""
活动相关仓储 - 使用 dataclasses DTO
"""
from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy import func, and_
from sqlalchemy.orm import Session
from baby_tracker.models.dto import (
    PlaytimeDTO, BathDTO, PhotoDTO, VideoDTO
)
from baby_tracker.models.mappers import (
    PlaytimeMapper, BathMapper, PhotoMapper, VideoMapper
)
from baby_tracker.repositories.base_repository import BaseRepository


class PlaytimeRepository(BaseRepository[PlaytimeDTO, 'Playtime']):
    """游戏时间仓储"""
    
    def _get_model_class(self):
        from baby_tracker.models.activity import Playtime
        return Playtime
    
    def _get_mapper(self):
        return PlaytimeMapper
    
    def find_by_baby_id(self, baby_id: str, limit: Optional[int] = None) -> List[PlaytimeDTO]:
        """根据宝宝ID查找游戏记录"""
        query = self.db_session.query(self.model_class).filter(
            self.model_class.baby_id == baby_id
        ).order_by(self.model_class.time.desc())
        
        if limit:
            query = query.limit(limit)
        
        model_instances = query.all()
        return [self.mapper.to_dto(instance) for instance in model_instances]
    
    def find_by_date_range(self, baby_id: str, start_date: datetime, end_date: datetime) -> List[PlaytimeDTO]:
        """根据日期范围查找游戏记录"""
        start_timestamp = start_date.timestamp()
        end_timestamp = end_date.timestamp()
        
        model_instances = self.db_session.query(self.model_class).filter(
            and_(
                self.model_class.baby_id == baby_id,
                self.model_class.time.between(start_timestamp, end_timestamp)
            )
        ).order_by(self.model_class.time.desc()).all()
        
        return [self.mapper.to_dto(instance) for instance in model_instances]
    
    def get_daily_playtime_duration(self, baby_id: str, date: datetime) -> int:
        """获取指定日期的游戏总时长（分钟）"""
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
    
    def get_playtime_by_type(self, baby_id: str, play_type: str, days: int = 30) -> List[PlaytimeDTO]:
        """获取指定类型的游戏记录"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        start_timestamp = start_date.timestamp()
        end_timestamp = end_date.timestamp()
        
        model_instances = self.db_session.query(self.model_class).filter(
            and_(
                self.model_class.baby_id == baby_id,
                self.model_class.time.between(start_timestamp, end_timestamp),
                self.model_class.play_type == play_type
            )
        ).order_by(self.model_class.time.desc()).all()
        
        return [self.mapper.to_dto(instance) for instance in model_instances]


class BathRepository(BaseRepository[BathDTO, 'Bath']):
    """洗澡记录仓储"""
    
    def _get_model_class(self):
        from baby_tracker.models.activity import Bath
        return Bath
    
    def _get_mapper(self):
        return BathMapper
    
    def find_by_baby_id(self, baby_id: str, limit: Optional[int] = None) -> List[BathDTO]:
        """根据宝宝ID查找洗澡记录"""
        query = self.db_session.query(self.model_class).filter(
            self.model_class.baby_id == baby_id
        ).order_by(self.model_class.time.desc())
        
        if limit:
            query = query.limit(limit)
        
        model_instances = query.all()
        return [self.mapper.to_dto(instance) for instance in model_instances]
    
    def find_by_date_range(self, baby_id: str, start_date: datetime, end_date: datetime) -> List[BathDTO]:
        """根据日期范围查找洗澡记录"""
        start_timestamp = start_date.timestamp()
        end_timestamp = end_date.timestamp()
        
        model_instances = self.db_session.query(self.model_class).filter(
            and_(
                self.model_class.baby_id == baby_id,
                self.model_class.time.between(start_timestamp, end_timestamp)
            )
        ).order_by(self.model_class.time.desc()).all()
        
        return [self.mapper.to_dto(instance) for instance in model_instances]
    
    def get_bath_frequency(self, baby_id: str, days: int = 30) -> float:
        """计算洗澡频率（每周次数）"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        start_timestamp = start_date.timestamp()
        end_timestamp = end_date.timestamp()
        
        bath_count = self.db_session.query(self.model_class).filter(
            and_(
                self.model_class.baby_id == baby_id,
                self.model_class.time.between(start_timestamp, end_timestamp)
            )
        ).count()
        
        weeks = days / 7
        return bath_count / weeks if weeks > 0 else 0


class PhotoRepository(BaseRepository[PhotoDTO, 'Photo']):
    """照片记录仓储"""
    
    def _get_model_class(self):
        from baby_tracker.models.activity import Photo
        return Photo
    
    def _get_mapper(self):
        return PhotoMapper
    
    def find_by_baby_id(self, baby_id: str, limit: Optional[int] = None) -> List[PhotoDTO]:
        """根据宝宝ID查找照片记录"""
        query = self.db_session.query(self.model_class).filter(
            self.model_class.baby_id == baby_id
        ).order_by(self.model_class.time.desc())
        
        if limit:
            query = query.limit(limit)
        
        model_instances = query.all()
        return [self.mapper.to_dto(instance) for instance in model_instances]
    
    def find_by_description(self, baby_id: str, keyword: str) -> List[PhotoDTO]:
        """根据关键词搜索照片描述"""
        model_instances = self.db_session.query(self.model_class).filter(
            and_(
                self.model_class.baby_id == baby_id,
                self.model_class.description.like(f"%{keyword}%")
            )
        ).order_by(self.model_class.time.desc()).all()
        
        return [self.mapper.to_dto(instance) for instance in model_instances]
    
    def get_photo_count_by_month(self, baby_id: str) -> dict:
        """按月统计照片数量"""
        result = {}
        
        # 获取所有照片记录
        photos = self.find_by_baby_id(baby_id)
        
        for photo in photos:
            photo_time = datetime.fromtimestamp(photo.time)
            month_key = f"{photo_time.year}-{photo_time.month:02d}"
            result[month_key] = result.get(month_key, 0) + 1
        
        return result


class VideoRepository(BaseRepository[VideoDTO, 'Video']):
    """视频记录仓储"""
    
    def _get_model_class(self):
        from baby_tracker.models.activity import Video
        return Video
    
    def _get_mapper(self):
        return VideoMapper
    
    def find_by_baby_id(self, baby_id: str, limit: Optional[int] = None) -> List[VideoDTO]:
        """根据宝宝ID查找视频记录"""
        query = self.db_session.query(self.model_class).filter(
            self.model_class.baby_id == baby_id
        ).order_by(self.model_class.time.desc())
        
        if limit:
            query = query.limit(limit)
        
        model_instances = query.all()
        return [self.mapper.to_dto(instance) for instance in model_instances]
    
    def find_by_description(self, baby_id: str, keyword: str) -> List[VideoDTO]:
        """根据关键词搜索视频描述"""
        model_instances = self.db_session.query(self.model_class).filter(
            and_(
                self.model_class.baby_id == baby_id,
                self.model_class.description.like(f"%{keyword}%")
            )
        ).order_by(self.model_class.time.desc()).all()
        
        return [self.mapper.to_dto(instance) for instance in model_instances]
    
    def get_total_video_duration(self, baby_id: str) -> int:
        """获取视频总时长（秒）"""
        result = self.db_session.query(func.sum(self.model_class.duration)).filter(
            self.model_class.baby_id == baby_id
        ).scalar()
        
        return result or 0
