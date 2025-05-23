"""
健康医疗相关模型
"""
from typing import Optional, TYPE_CHECKING
from sqlalchemy import Column, String, Float, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from baby_tracker.models.base import BaseModel

if TYPE_CHECKING:
    from baby_tracker.models.baby import Baby
    from baby_tracker.models.lookup import DiaperDesc, SleepDesc


class HealthMixin:
    """健康记录通用字段混入类"""
    
    # 重写ID字段以匹配现有数据库结构
    id = Column(String, primary_key=True, name='ID')
    timestamp = Column(Float, name='Timestamp')
    time = Column(Float, name='Time', nullable=False)  # 活动时间
    note = Column(Text, name='Note', nullable=True)
    has_picture = Column(Integer, name='HasPicture', default=0)
    baby_id = Column(String, ForeignKey('Baby.ID'), name='BabyID', nullable=False)


class Sleep(BaseModel, HealthMixin):
    """睡眠记录表"""
    
    __tablename__ = 'Sleep'
    
    # 睡眠描述（开始睡觉/醒来等）
    desc_id = Column(String, ForeignKey('SleepDesc.ID'), name='DescID', nullable=True)
    
    # 睡眠时长（分钟）
    duration = Column(Integer, name='Duration', default=0)
    
    # 关系
    baby: "Baby" = relationship("Baby", back_populates="sleep_records")
    sleep_desc: Optional["SleepDesc"] = relationship("SleepDesc")


class Diaper(BaseModel, HealthMixin):
    """尿布记录表"""
    
    __tablename__ = 'Diaper'
    
    # 尿布类型描述
    desc_id = Column(String, ForeignKey('DiaperDesc.ID'), name='DescID', nullable=True)
    
    # 关系
    baby: "Baby" = relationship("Baby", back_populates="diaper_records")
    diaper_desc: Optional["DiaperDesc"] = relationship("DiaperDesc")


class Height(BaseModel, HealthMixin):
    """身高记录表"""
    
    __tablename__ = 'Height'
    
    # 身高值（厘米）
    height = Column(Float, name='Height', nullable=False)
    
    # 关系
    baby: "Baby" = relationship("Baby", back_populates="height_records")


class Weight(BaseModel, HealthMixin):
    """体重记录表"""
    
    __tablename__ = 'Weight'
    
    # 体重值（克）
    weight = Column(Float, name='Weight', nullable=False)
    
    # 关系
    baby: "Baby" = relationship("Baby", back_populates="weight_records")


class Head(BaseModel, HealthMixin):
    """头围记录表"""
    
    __tablename__ = 'Head'
    
    # 头围值（厘米）
    head = Column(Float, name='Head', nullable=False)
    
    # 关系
    baby: "Baby" = relationship("Baby", back_populates="head_records")


class Temperature(BaseModel, HealthMixin):
    """体温记录表"""
    
    __tablename__ = 'Temperature'
    
    # 体温值（摄氏度）
    temperature = Column(Float, name='Temperature', nullable=False)
    
    # 测量位置（口腔、腋下、额头等）
    location = Column(String, name='Location', nullable=True)
    
    # 关系
    baby: "Baby" = relationship("Baby", back_populates="temperature_records")
    
    @property
    def is_fever(self) -> bool:
        """判断是否发烧（基于腋下体温37.5°C）"""
        return self.temperature >= 37.5
    
    @property
    def temperature_status(self) -> str:
        """体温状态"""
        if self.temperature < 36.0:
            return "偏低"
        elif self.temperature <= 37.0:
            return "正常"
        elif self.temperature <= 37.5:
            return "稍高"
        else:
            return "发烧"
