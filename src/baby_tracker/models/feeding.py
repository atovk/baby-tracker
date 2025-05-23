"""
喂养相关模型
"""
from typing import Optional, TYPE_CHECKING
from sqlalchemy import Column, String, Float, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from baby_tracker.models.base import BaseModel

if TYPE_CHECKING:
    from baby_tracker.models.baby import Baby
    from baby_tracker.models.lookup import FeedDesc


class FeedingMixin:
    """喂养记录通用字段混入类"""
    
    # 重写ID字段以匹配现有数据库结构
    id = Column(String, primary_key=True, name='ID')
    timestamp = Column(Float, name='Timestamp')
    time = Column(Float, name='Time', nullable=False)  # 活动时间
    note = Column(Text, name='Note', nullable=True)
    has_picture = Column(Integer, name='HasPicture', default=0)
    baby_id = Column(String, ForeignKey('Baby.ID'), name='BabyID', nullable=False)


class Nursing(BaseModel, FeedingMixin):
    """母乳喂养记录表"""
    
    __tablename__ = 'Nursing'
    
    # 喂养描述（可能关联到FeedDesc表）
    desc_id = Column(String, ForeignKey('FeedDesc.ID'), name='DescID', nullable=True)
    
    # 结束的一侧（0=左侧, 1=右侧, 2=两侧/未知）
    finish_side = Column(Integer, name='FinishSide', default=2)
    
    # 各侧喂养时长（分钟）
    left_duration = Column(Integer, name='LeftDuration', default=0)
    right_duration = Column(Integer, name='RightDuration', default=0)
    both_duration = Column(Integer, name='BothDuration', default=0)
    
    # 关系
    baby: "Baby" = relationship("Baby", back_populates="nursing_sessions")
    feed_desc: Optional["FeedDesc"] = relationship("FeedDesc")
    
    @property
    def total_duration(self) -> int:
        """总喂养时长"""
        return self.left_duration + self.right_duration + self.both_duration
    
    @property
    def finish_side_display(self) -> str:
        """结束侧的显示文本"""
        sides = {0: "左侧", 1: "右侧", 2: "两侧/未知"}
        return sides.get(self.finish_side, "未知")


class Formula(BaseModel, FeedingMixin):
    """配方奶喂养记录表"""
    
    __tablename__ = 'Formula'
    
    # 喂养描述
    desc_id = Column(String, ForeignKey('FeedDesc.ID'), name='DescID', nullable=True)
    
    # 配方奶量（毫升）
    amount = Column(Float, name='Amount', default=0.0)
    
    # 关系
    baby: "Baby" = relationship("Baby", back_populates="formula_sessions")
    feed_desc: Optional["FeedDesc"] = relationship("FeedDesc")


class Pumping(BaseModel, FeedingMixin):
    """吸奶记录表"""
    
    __tablename__ = 'Pumping'
    
    # 喂养描述
    desc_id = Column(String, ForeignKey('FeedDesc.ID'), name='DescID', nullable=True)
    
    # 吸奶量（毫升）
    amount = Column(Float, name='Amount', default=0.0)
    
    # 吸奶时长（分钟）
    duration = Column(Integer, name='Duration', default=0)
    
    # 关系
    baby: "Baby" = relationship("Baby", back_populates="pumping_sessions")
    feed_desc: Optional["FeedDesc"] = relationship("FeedDesc")


class Solids(BaseModel, FeedingMixin):
    """辅食记录表"""
    
    __tablename__ = 'Solids'
    
    # 喂养描述
    desc_id = Column(String, ForeignKey('FeedDesc.ID'), name='DescID', nullable=True)
    
    # 食物量（可以是估计量）
    amount = Column(Float, name='Amount', default=0.0)
    
    # 关系
    baby: "Baby" = relationship("Baby", back_populates="solid_feeding_sessions")
    feed_desc: Optional["FeedDesc"] = relationship("FeedDesc")
