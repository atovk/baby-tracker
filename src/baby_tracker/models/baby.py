"""
宝宝信息模型 - 使用 dataclasses 重构
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import Column, String, Float, Integer, Text
from sqlalchemy.orm import relationship
from baby_tracker.models.base import BaseModel

if TYPE_CHECKING:
    from baby_tracker.models.feeding import Nursing, Formula, Pumping, Solids
    from baby_tracker.models.health import Sleep, Diaper, Height, Weight, Head, Temperature
    from baby_tracker.models.activity import Playtime, Bath, Photo, Video


@dataclass
class Baby(BaseModel):
    """宝宝信息表 - 使用 dataclasses"""
    
    __tablename__ = 'Baby'
    
    # 基本信息字段
    name: str = field(default="")
    dob: float = field(default=0.0)  # Date of Birth (Unix timestamp)
    due_day: Optional[str] = field(default=None)
    gender: int = field(default=0)  # 0=female, 1=male
    picture: Optional[str] = field(default=None)
    
    # SQLAlchemy 列映射（保持与现有数据库兼容）
    def __post_init__(self):
        if not hasattr(self.__class__, '_sa_columns_defined'):
            # 重写ID字段以匹配现有数据库结构
            self.__class__.id = Column(String, primary_key=True, name='ID')
            self.__class__.timestamp = Column(Float, name='Timestamp')
            self.__class__.name = Column(String, name='Name', nullable=False)
            self.__class__.dob = Column(Float, name='DOB', nullable=False)
            self.__class__.due_day = Column(String, name='DueDay', nullable=True)
            self.__class__.gender = Column(Integer, name='Gender', nullable=False)
            self.__class__.picture = Column(String, name='Picture', nullable=True)
            
            # 关系定义 - 喂养相关
            self.__class__.nursing_sessions: List["Nursing"] = relationship(
                "Nursing", back_populates="baby", cascade="all, delete-orphan"
            )
            self.__class__.formula_sessions: List["Formula"] = relationship(
                "Formula", back_populates="baby", cascade="all, delete-orphan"
            )
            self.__class__.pumping_sessions: List["Pumping"] = relationship(
                "Pumping", back_populates="baby", cascade="all, delete-orphan"
            )
            self.__class__.solid_feeding_sessions: List["Solids"] = relationship(
                "Solids", back_populates="baby", cascade="all, delete-orphan"
            )
            
            # 关系定义 - 健康相关
            self.__class__.sleep_records: List["Sleep"] = relationship(
                "Sleep", back_populates="baby", cascade="all, delete-orphan"
            )
            self.__class__.diaper_records: List["Diaper"] = relationship(
                "Diaper", back_populates="baby", cascade="all, delete-orphan"
            )
            self.__class__.height_records: List["Height"] = relationship(
                "Height", back_populates="baby", cascade="all, delete-orphan"
            )
            self.__class__.weight_records: List["Weight"] = relationship(
                "Weight", back_populates="baby", cascade="all, delete-orphan"
            )
            self.__class__.head_records: List["Head"] = relationship(
                "Head", back_populates="baby", cascade="all, delete-orphan"
            )
            self.__class__.temperature_records: List["Temperature"] = relationship(
                "Temperature", back_populates="baby", cascade="all, delete-orphan"
            )
            
            # 关系定义 - 活动相关
            self.__class__.playtime_records: List["Playtime"] = relationship(
                "Playtime", back_populates="baby", cascade="all, delete-orphan"
            )
            self.__class__.bath_records: List["Bath"] = relationship(
                "Bath", back_populates="baby", cascade="all, delete-orphan"
            )
            self.__class__.photos: List["Photo"] = relationship(
                "Photo", back_populates="baby", cascade="all, delete-orphan"
            )
            self.__class__.videos: List["Video"] = relationship(
                "Video", back_populates="baby", cascade="all, delete-orphan"
            )
            
            self.__class__._sa_columns_defined = True
    
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
    
    def get_latest_weight(self) -> Optional[float]:
        """获取最新体重"""
        if hasattr(self, 'weight_records') and self.weight_records:
            return max(self.weight_records, key=lambda x: x.time).weight
        return None
    
    def get_latest_height(self) -> Optional[float]:
        """获取最新身高"""
        if hasattr(self, 'height_records') and self.height_records:
            return max(self.height_records, key=lambda x: x.time).height
        return None
    
    def __repr__(self) -> str:
        return f"<Baby(id={self.id}, name={self.name}, age_days={self.age_in_days})>"
