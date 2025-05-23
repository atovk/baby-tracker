"""
查找表模型 - 使用 dataclasses 和 SQLAlchemy 混合模式
"""
from dataclasses import dataclass, field
from typing import Optional
from sqlalchemy import Column, String, Integer, Text
from baby_tracker.models.base import BaseModel


@dataclass
class FeedDesc(BaseModel):
    """喂养描述查找表"""
    
    __tablename__ = 'FeedDesc'
    
    # 重写ID字段以匹配现有数据库结构
    id: str = field(default_factory=str)
    name: str = field(default="")
    description: Optional[str] = field(default=None)
    category: str = field(default="")  # nursing, formula, pumping, solids
    
    def __post_init__(self):
        # SQLAlchemy 列定义
        if not hasattr(self.__class__, '_sa_columns_defined'):
            self.id = Column(String, primary_key=True, name='ID')
            self.name = Column(String, name='Name', nullable=False)
            self.description = Column(Text, name='Description', nullable=True)
            self.category = Column(String, name='Category', nullable=False)
            self.__class__._sa_columns_defined = True


@dataclass
class DiaperDesc(BaseModel):
    """尿布类型描述查找表"""
    
    __tablename__ = 'DiaperDesc'
    
    id: str = field(default_factory=str)
    name: str = field(default="")
    description: Optional[str] = field(default=None)
    
    def __post_init__(self):
        if not hasattr(self.__class__, '_sa_columns_defined'):
            self.id = Column(String, primary_key=True, name='ID')
            self.name = Column(String, name='Name', nullable=False)
            self.description = Column(Text, name='Description', nullable=True)
            self.__class__._sa_columns_defined = True


@dataclass
class SleepDesc(BaseModel):
    """睡眠描述查找表"""
    
    __tablename__ = 'SleepDesc'
    
    id: str = field(default_factory=str)
    name: str = field(default="")
    description: Optional[str] = field(default=None)
    
    def __post_init__(self):
        if not hasattr(self.__class__, '_sa_columns_defined'):
            self.id = Column(String, primary_key=True, name='ID')
            self.name = Column(String, name='Name', nullable=False)
            self.description = Column(Text, name='Description', nullable=True)
            self.__class__._sa_columns_defined = True
