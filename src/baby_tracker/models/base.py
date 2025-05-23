"""
基础模型类
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, Float, Integer, Text, Boolean
from sqlalchemy.ext.declarative import declared_attr
from baby_tracker.database import Base
import uuid


class TimestampMixin:
    """时间戳混入类"""
    
    @declared_attr
    def timestamp(cls):
        """记录创建或更新时间戳"""
        return Column(Float, default=lambda: datetime.now().timestamp())


class BaseModel(Base, TimestampMixin):
    """基础模型类"""
    
    __abstract__ = True
    
    @declared_attr
    def id(cls):
        """主键ID"""
        return Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    def to_dict(self) -> dict:
        """转换为字典"""
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if isinstance(value, datetime):
                value = value.timestamp()
            result[column.name] = value
        return result
    
    @classmethod
    def from_dict(cls, data: dict):
        """从字典创建实例"""
        # 过滤掉不存在的字段
        valid_data = {}
        for key, value in data.items():
            if hasattr(cls, key):
                valid_data[key] = value
        return cls(**valid_data)


class ActivityMixin:
    """活动记录混入类"""
    
    @declared_attr
    def time(cls):
        """活动发生时间"""
        return Column(Float, nullable=False)
    
    @declared_attr
    def note(cls):
        """备注"""
        return Column(Text)
    
    @declared_attr
    def has_picture(cls):
        """是否有图片"""
        return Column(Integer, default=0)
    
    @declared_attr
    def baby_id(cls):
        """关联的宝宝ID"""
        return Column(String, nullable=False, index=True)


class LookupMixin:
    """查找表混入类"""
    
    @declared_attr
    def name(cls):
        """名称"""
        return Column(String, nullable=False)
    
    @declared_attr
    def description(cls):
        """描述"""
        return Column(Text)
