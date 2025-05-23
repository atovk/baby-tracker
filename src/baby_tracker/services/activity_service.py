"""
活动服务 - 提供活动相关的业务逻辑
"""
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import uuid
import os
from sqlalchemy.orm import Session
from baby_tracker.models.dto import (
    PlaytimeDTO, BathDTO, PhotoDTO, VideoDTO
)
from baby_tracker.repositories import (
    PlaytimeRepository, BathRepository, PhotoRepository, VideoRepository
)


class ActivityService:
    """活动服务"""
    
    def __init__(self, db_session: Optional[Session] = None):
        from baby_tracker.database import get_db
        self.db_session = db_session or next(get_db())
        self.playtime_repo = PlaytimeRepository(self.db_session)
        self.bath_repo = BathRepository(self.db_session)
        self.photo_repo = PhotoRepository(self.db_session)
        self.video_repo = VideoRepository(self.db_session)
    
    # Playtime 相关方法
    def add_playtime_record(self, baby_id: str, duration: int, 
                           play_type: Optional[str] = None,
                           note: Optional[str] = None, 
                           time: Optional[float] = None) -> PlaytimeDTO:
        """添加游戏时间记录"""
        playtime_dto = PlaytimeDTO(
            id=str(uuid.uuid4()),
            baby_id=baby_id,
            duration=duration,
            play_type=play_type,
            note=note,
            time=time or datetime.now().timestamp()
        )
        
        return self.playtime_repo.create(playtime_dto)
    
    def get_playtime_records(self, baby_id: str, limit: Optional[int] = None) -> List[PlaytimeDTO]:
        """获取宝宝的游戏记录"""
        return self.playtime_repo.find_by_baby_id(baby_id, limit)
    
    def get_playtime_stats(self, baby_id: str, days: int = 7) -> Dict[str, Any]:
        """获取游戏统计数据"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # 获取日期范围内的所有游戏记录
        playtime_records = self.playtime_repo.find_by_date_range(baby_id, start_date, end_date)
        
        # 按日期和类型分组
        daily_playtime = {}
        play_types = {}
        
        for record in playtime_records:
            day = datetime.fromtimestamp(record.time).strftime('%Y-%m-%d')
            if day not in daily_playtime:
                daily_playtime[day] = 0
            
            daily_playtime[day] += record.duration
            
            if record.play_type:
                play_types[record.play_type] = play_types.get(record.play_type, 0) + record.duration
        
        # 计算统计数据
        total_duration = sum(daily_playtime.values())
        avg_duration = total_duration / len(daily_playtime) if daily_playtime else 0
        
        return {
            'daily_playtime': daily_playtime,  # 每日游戏时长（分钟）
            'play_types': play_types,  # 各类型游戏时长
            'total_duration': total_duration,  # 总游戏时长（分钟）
            'avg_daily_duration': avg_duration,  # 平均每日游戏时长（分钟）
            'record_count': len(playtime_records)  # 记录数量
        }
    
    # Bath 相关方法
    def add_bath_record(self, baby_id: str, duration: int, 
                       water_temperature: Optional[float] = None,
                       note: Optional[str] = None, 
                       time: Optional[float] = None) -> BathDTO:
        """添加洗澡记录"""
        bath_dto = BathDTO(
            id=str(uuid.uuid4()),
            baby_id=baby_id,
            duration=duration,
            water_temperature=water_temperature,
            note=note,
            time=time or datetime.now().timestamp()
        )
        
        return self.bath_repo.create(bath_dto)
    
    def get_bath_records(self, baby_id: str, limit: Optional[int] = None) -> List[BathDTO]:
        """获取宝宝的洗澡记录"""
        return self.bath_repo.find_by_baby_id(baby_id, limit)
    
    def get_bath_stats(self, baby_id: str, days: int = 30) -> Dict[str, Any]:
        """获取洗澡统计数据"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # 获取日期范围内的所有洗澡记录
        bath_records = self.bath_repo.find_by_date_range(baby_id, start_date, end_date)
        
        # 计算统计数据
        bath_count = len(bath_records)
        bath_frequency = bath_count / (days / 7)  # 每周次数
        
        # 计算平均洗澡时长和平均水温
        total_duration = sum(record.duration for record in bath_records)
        avg_duration = total_duration / bath_count if bath_count else 0
        
        temperatures = [record.water_temperature for record in bath_records if record.water_temperature]
        avg_temperature = sum(temperatures) / len(temperatures) if temperatures else None
        
        return {
            'bath_count': bath_count,
            'bath_frequency': bath_frequency,  # 每周洗澡次数
            'avg_duration': avg_duration,  # 平均洗澡时长（分钟）
            'avg_temperature': avg_temperature  # 平均水温
        }
    
    # Photo 相关方法
    def add_photo_record(self, baby_id: str, file_path: str, 
                        description: Optional[str] = None,
                        note: Optional[str] = None, 
                        time: Optional[float] = None) -> PhotoDTO:
        """添加照片记录"""
        # 确保文件存在
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"照片文件不存在: {file_path}")
        
        photo_dto = PhotoDTO(
            id=str(uuid.uuid4()),
            baby_id=baby_id,
            file_path=file_path,
            description=description,
            note=note,
            has_picture=True,
            time=time or datetime.now().timestamp()
        )
        
        return self.photo_repo.create(photo_dto)
    
    def get_photo_records(self, baby_id: str, limit: Optional[int] = None) -> List[PhotoDTO]:
        """获取宝宝的照片记录"""
        return self.photo_repo.find_by_baby_id(baby_id, limit)
    
    def search_photos(self, baby_id: str, keyword: str) -> List[PhotoDTO]:
        """搜索照片"""
        return self.photo_repo.find_by_description(baby_id, keyword)
    
    # Video 相关方法
    def add_video_record(self, baby_id: str, file_path: str, 
                        duration: int,
                        description: Optional[str] = None,
                        note: Optional[str] = None, 
                        time: Optional[float] = None) -> VideoDTO:
        """添加视频记录"""
        # 确保文件存在
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"视频文件不存在: {file_path}")
        
        video_dto = VideoDTO(
            id=str(uuid.uuid4()),
            baby_id=baby_id,
            file_path=file_path,
            duration=duration,
            description=description,
            note=note,
            has_picture=True,
            time=time or datetime.now().timestamp()
        )
        
        return self.video_repo.create(video_dto)
    
    def get_video_records(self, baby_id: str, limit: Optional[int] = None) -> List[VideoDTO]:
        """获取宝宝的视频记录"""
        return self.video_repo.find_by_baby_id(baby_id, limit)
    
    def search_videos(self, baby_id: str, keyword: str) -> List[VideoDTO]:
        """搜索视频"""
        return self.video_repo.find_by_description(baby_id, keyword)
    
    def get_media_stats(self, baby_id: str) -> Dict[str, Any]:
        """获取媒体统计数据"""
        # 获取照片统计
        photos = self.photo_repo.find_by_baby_id(baby_id)
        photo_count = len(photos)
        photo_count_by_month = self.photo_repo.get_photo_count_by_month(baby_id)
        
        # 获取视频统计
        videos = self.video_repo.find_by_baby_id(baby_id)
        video_count = len(videos)
        total_video_duration = self.video_repo.get_total_video_duration(baby_id)
        
        return {
            'photo_count': photo_count,
            'photo_count_by_month': photo_count_by_month,
            'video_count': video_count,
            'total_video_duration_seconds': total_video_duration,
            'total_video_duration_minutes': total_video_duration / 60 if total_video_duration else 0
        }
