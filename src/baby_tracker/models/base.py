"""
基础模型类 - 使用 dataclasses 重构
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy import Column, String, Float, Integer, Text, Boolean
from sqlalchemy.ext.declarative import declared_attr
from baby_tracker.database import Base
import uuid


@dataclass
class TimestampMixin:
    """时间戳混入类"""
    
    timestamp: float = field(default_factory=lambda: datetime.now().timestamp())
    
    @declared_attr
    def timestamp_column(cls):
        """记录创建或更新时间戳的SQLAlchemy列"""
        return Column(Float, default=lambda: datetime.now().timestamp())


@dataclass
class BaseModel(Base, TimestampMixin):
    """基础模型类 - 使用 dataclasses"""
    
    __abstract__ = True
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    
    @declared_attr
    def id_column(cls):
        """主键ID的SQLAlchemy列"""
        return Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        result = {}
        for field_name in self.__dataclass_fields__.keys():
            value = getattr(self, field_name)
            if isinstance(value, datetime):
                value = value.timestamp()
            result[field_name] = value
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """从字典创建实例"""
        # 过滤掉不存在的字段
        valid_data = {}
        for key, value in data.items():
            if key in cls.__dataclass_fields__:
                valid_data[key] = value
        return cls(**valid_data)
    
    def update_from_dict(self, data: Dict[str, Any]) -> None:
        """从字典更新实例"""
        for key, value in data.items():
            if key in self.__dataclass_fields__ and hasattr(self, key):
                setattr(self, key, value)


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
