"""
活动记录相关模型
"""
from typing import Optional, TYPE_CHECKING
from sqlalchemy import Column, String, Float, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from baby_tracker.models.base import BaseModel

if TYPE_CHECKING:
    from baby_tracker.models.baby import Baby


class ActivityMixin:
    """活动记录通用字段混入类"""
    
    # 重写ID字段以匹配现有数据库结构
    id = Column(String, primary_key=True, name='ID')
    timestamp = Column(Float, name='Timestamp')
    time = Column(Float, name='Time', nullable=False)  # 活动时间
    note = Column(Text, name='Note', nullable=True)
    has_picture = Column(Integer, name='HasPicture', default=0)
    baby_id = Column(String, ForeignKey('Baby.ID'), name='BabyID', nullable=False)


class Playtime(BaseModel, ActivityMixin):
    """游戏时间记录表"""
    
    __tablename__ = 'Playtime'
    
    # 游戏时长（分钟）
    duration = Column(Integer, name='Duration', default=0)
    
    # 游戏类型
    play_type = Column(String, name='PlayType', nullable=True)
    
    # 关系
    baby: "Baby" = relationship("Baby", back_populates="playtime_records")


class Bath(BaseModel, ActivityMixin):
    """洗澡记录表"""
    
    __tablename__ = 'Bath'
    
    # 洗澡时长（分钟）
    duration = Column(Integer, name='Duration', default=0)
    
    # 水温
    water_temperature = Column(Float, name='WaterTemperature', nullable=True)
    
    # 关系
    baby: "Baby" = relationship("Baby", back_populates="bath_records")


class Photo(BaseModel, ActivityMixin):
    """照片记录表"""
    
    __tablename__ = 'Photo'
    
    # 照片文件路径
    file_path = Column(String, name='FilePath', nullable=False)
    
    # 照片描述/标签
    description = Column(Text, name='Description', nullable=True)
    
    # 关系
    baby: "Baby" = relationship("Baby", back_populates="photos")


class Video(BaseModel, ActivityMixin):
    """视频记录表"""
    
    __tablename__ = 'Video'
    
    # 视频文件路径
    file_path = Column(String, name='FilePath', nullable=False)
    
    # 视频时长（秒）
    duration = Column(Integer, name='Duration', default=0)
    
    # 视频描述/标签
    description = Column(Text, name='Description', nullable=True)
    
    # 关系
    baby: "Baby" = relationship("Baby", back_populates="videos")
