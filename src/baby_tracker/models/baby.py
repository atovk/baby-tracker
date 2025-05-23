"""
宝宝信息模型
"""
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import Column, String, Float, Integer, Text
from sqlalchemy.orm import relationship
from baby_tracker.models.base import BaseModel

if TYPE_CHECKING:
    from baby_tracker.models.feeding import Nursing, Formula, Pumping, Solids
    from baby_tracker.models.health import Sleep, Diaper, Height, Weight, Head, Temperature
    from baby_tracker.models.activity import Playtime, Bath, Photo, Video


class Baby(BaseModel):
    """宝宝信息表"""
    
    __tablename__ = 'Baby'
    
    # 重写ID字段以匹配现有数据库结构
    id = Column(String, primary_key=True, name='ID')
    timestamp = Column(Float, name='Timestamp')
    
    # 基本信息
    name = Column(String, name='Name', nullable=False)
    dob = Column(Float, name='DOB', nullable=False)  # Date of Birth (Unix timestamp)
    due_day = Column(String, name='DueDay', nullable=True)
    gender = Column(Integer, name='Gender', nullable=False)  # 0=female, 1=male
    picture = Column(String, name='Picture', nullable=True)
    
    # 关系定义 - 喂养相关
    nursing_sessions: List["Nursing"] = relationship(
        "Nursing", back_populates="baby", cascade="all, delete-orphan"
    )
    formula_sessions: List["Formula"] = relationship(
        "Formula", back_populates="baby", cascade="all, delete-orphan"
    )
    pumping_sessions: List["Pumping"] = relationship(
        "Pumping", back_populates="baby", cascade="all, delete-orphan"
    )
    solid_feeding_sessions: List["Solids"] = relationship(
        "Solids", back_populates="baby", cascade="all, delete-orphan"
    )
    
    # 关系定义 - 健康相关
    sleep_records: List["Sleep"] = relationship(
        "Sleep", back_populates="baby", cascade="all, delete-orphan"
    )
    diaper_records: List["Diaper"] = relationship(
        "Diaper", back_populates="baby", cascade="all, delete-orphan"
    )
    height_records: List["Height"] = relationship(
        "Height", back_populates="baby", cascade="all, delete-orphan"
    )
    weight_records: List["Weight"] = relationship(
        "Weight", back_populates="baby", cascade="all, delete-orphan"
    )
    head_records: List["Head"] = relationship(
        "Head", back_populates="baby", cascade="all, delete-orphan"
    )
    temperature_records: List["Temperature"] = relationship(
        "Temperature", back_populates="baby", cascade="all, delete-orphan"
    )
    
    # 关系定义 - 活动相关
    playtime_records: List["Playtime"] = relationship(
        "Playtime", back_populates="baby", cascade="all, delete-orphan"
    )
    bath_records: List["Bath"] = relationship(
        "Bath", back_populates="baby", cascade="all, delete-orphan"
    )
    photos: List["Photo"] = relationship(
        "Photo", back_populates="baby", cascade="all, delete-orphan"
    )
    videos: List["Video"] = relationship(
        "Video", back_populates="baby", cascade="all, delete-orphan"
    )
    
    @property
    def age_in_days(self) -> int:
        """计算宝宝的天数"""
        if self.dob:
            birth_date = datetime.fromtimestamp(self.dob)
            return (datetime.now() - birth_date).days
        return 0
    
    @property
    def age_in_weeks(self) -> int:
        """计算宝宝的周数"""
        return self.age_in_days // 7
    
    @property
    def age_in_months(self) -> int:
        """计算宝宝的月数（粗略）"""
        return self.age_in_days // 30
    
    @property
    def gender_display(self) -> str:
        """返回性别的显示文本"""
        return "女孩" if self.gender == 0 else "男孩"
    
    def __repr__(self) -> str:
        return f"<Baby(id={self.id}, name={self.name}, age_days={self.age_in_days})>"
