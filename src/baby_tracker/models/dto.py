"""
数据传输对象 (DTO) - 使用 dataclasses
这些类用于在服务层和API层之间传输数据
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from enum import Enum


class Gender(Enum):
    """性别枚举"""
    FEMALE = 0
    MALE = 1


class FinishSide(Enum):
    """喂养结束侧枚举"""
    LEFT = 0
    RIGHT = 1
    BOTH_UNKNOWN = 2


@dataclass
class BabyDTO:
    """宝宝信息数据传输对象"""
    id: str = ""
    name: str = ""
    dob: float = 0.0  # Unix timestamp
    due_day: Optional[str] = None
    gender: Gender = Gender.FEMALE
    picture: Optional[str] = None
    timestamp: float = field(default_factory=lambda: datetime.now().timestamp())
    
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
        return "女孩" if self.gender == Gender.FEMALE else "男孩"
    
    @property
    def birth_date(self) -> datetime:
        """出生日期"""
        return datetime.fromtimestamp(self.dob) if self.dob else datetime.now()


@dataclass
class NursingDTO:
    """母乳喂养记录数据传输对象"""
    id: str = ""
    baby_id: str = ""
    time: float = 0.0
    note: Optional[str] = None
    has_picture: bool = False
    desc_id: Optional[str] = None
    finish_side: FinishSide = FinishSide.BOTH_UNKNOWN
    left_duration: int = 0  # 分钟
    right_duration: int = 0  # 分钟
    both_duration: int = 0  # 分钟
    timestamp: float = field(default_factory=lambda: datetime.now().timestamp())
    
    @property
    def total_duration(self) -> int:
        """总喂养时长"""
        return self.left_duration + self.right_duration + self.both_duration
    
    @property
    def finish_side_display(self) -> str:
        """结束侧的显示文本"""
        mapping = {
            FinishSide.LEFT: "左侧",
            FinishSide.RIGHT: "右侧",
            FinishSide.BOTH_UNKNOWN: "两侧/未知"
        }
        return mapping[self.finish_side]
    
    @property
    def feeding_time(self) -> datetime:
        """喂养时间"""
        return datetime.fromtimestamp(self.time)


@dataclass
class FormulaDTO:
    """配方奶喂养记录数据传输对象"""
    id: str = ""
    baby_id: str = ""
    time: float = 0.0
    note: Optional[str] = None
    has_picture: bool = False
    desc_id: Optional[str] = None
    amount: float = 0.0  # 毫升
    timestamp: float = field(default_factory=lambda: datetime.now().timestamp())
    
    @property
    def feeding_time(self) -> datetime:
        """喂养时间"""
        return datetime.fromtimestamp(self.time)


@dataclass
class SleepDTO:
    """睡眠记录数据传输对象"""
    id: str = ""
    baby_id: str = ""
    time: float = 0.0
    note: Optional[str] = None
    has_picture: bool = False
    desc_id: Optional[str] = None
    duration: int = 0  # 分钟
    timestamp: float = field(default_factory=lambda: datetime.now().timestamp())
    
    @property
    def sleep_time(self) -> datetime:
        """睡眠时间"""
        return datetime.fromtimestamp(self.time)
    
    @property
    def duration_hours(self) -> float:
        """睡眠时长（小时）"""
        return self.duration / 60.0


@dataclass
class DiaperDTO:
    """尿布记录数据传输对象"""
    id: str = ""
    baby_id: str = ""
    time: float = 0.0
    note: Optional[str] = None
    has_picture: bool = False
    desc_id: Optional[str] = None
    timestamp: float = field(default_factory=lambda: datetime.now().timestamp())
    
    @property
    def change_time(self) -> datetime:
        """换尿布时间"""
        return datetime.fromtimestamp(self.time)


@dataclass
class WeightDTO:
    """体重记录数据传输对象"""
    id: str = ""
    baby_id: str = ""
    time: float = 0.0
    note: Optional[str] = None
    has_picture: bool = False
    weight: float = 0.0  # 克
    timestamp: float = field(default_factory=lambda: datetime.now().timestamp())
    
    @property
    def weight_kg(self) -> float:
        """体重（公斤）"""
        return self.weight / 1000.0
    
    @property
    def measurement_time(self) -> datetime:
        """测量时间"""
        return datetime.fromtimestamp(self.time)


@dataclass
class HeightDTO:
    """身高记录数据传输对象"""
    id: str = ""
    baby_id: str = ""
    time: float = 0.0
    note: Optional[str] = None
    has_picture: bool = False
    height: float = 0.0  # 厘米
    timestamp: float = field(default_factory=lambda: datetime.now().timestamp())
    
    @property
    def measurement_time(self) -> datetime:
        """测量时间"""
        return datetime.fromtimestamp(self.time)


@dataclass
class TemperatureDTO:
    """体温记录数据传输对象"""
    id: str = ""
    baby_id: str = ""
    time: float = 0.0
    note: Optional[str] = None
    has_picture: bool = False
    temperature: float = 0.0  # 摄氏度
    location: Optional[str] = None  # 测量位置
    timestamp: float = field(default_factory=lambda: datetime.now().timestamp())
    
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
    
    @property
    def measurement_time(self) -> datetime:
        """测量时间"""
        return datetime.fromtimestamp(self.time)


@dataclass
class FeedingStatsDTO:
    """喂养统计数据传输对象"""
    baby_id: str
    date: datetime
    total_nursing_sessions: int = 0
    total_nursing_duration: int = 0  # 分钟
    total_formula_amount: float = 0.0  # 毫升
    total_formula_sessions: int = 0
    average_session_duration: float = 0.0  # 分钟
    
    @property
    def total_feeding_sessions(self) -> int:
        """总喂养次数"""
        return self.total_nursing_sessions + self.total_formula_sessions


@dataclass
class GrowthStatsDTO:
    """成长统计数据传输对象"""
    baby_id: str
    latest_weight: Optional[float] = None  # 克
    latest_height: Optional[float] = None  # 厘米
    latest_head: Optional[float] = None  # 厘米
    weight_trend: str = "stable"  # increasing, decreasing, stable
    height_trend: str = "stable"
    
    @property
    def latest_weight_kg(self) -> Optional[float]:
        """最新体重（公斤）"""
        return self.latest_weight / 1000.0 if self.latest_weight else None


@dataclass
class HeadDTO:
    """头围记录数据传输对象"""
    id: str = ""
    baby_id: str = ""
    time: float = 0.0
    note: Optional[str] = None
    has_picture: bool = False
    head: float = 0.0  # 厘米
    timestamp: float = field(default_factory=lambda: datetime.now().timestamp())
    
    @property
    def measurement_time(self) -> datetime:
        """测量时间"""
        return datetime.fromtimestamp(self.time)


@dataclass
class PlaytimeDTO:
    """游戏时间记录数据传输对象"""
    id: str = ""
    baby_id: str = ""
    time: float = 0.0
    note: Optional[str] = None
    has_picture: bool = False
    duration: int = 0  # 分钟
    play_type: Optional[str] = None  # 游戏类型
    timestamp: float = field(default_factory=lambda: datetime.now().timestamp())
    
    @property
    def play_time(self) -> datetime:
        """游戏时间"""
        return datetime.fromtimestamp(self.time)
    
    @property
    def duration_hours(self) -> float:
        """游戏时长（小时）"""
        return self.duration / 60.0


@dataclass
class BathDTO:
    """洗澡记录数据传输对象"""
    id: str = ""
    baby_id: str = ""
    time: float = 0.0
    note: Optional[str] = None
    has_picture: bool = False
    duration: int = 0  # 分钟
    water_temperature: Optional[float] = None  # 水温
    timestamp: float = field(default_factory=lambda: datetime.now().timestamp())
    
    @property
    def bath_time(self) -> datetime:
        """洗澡时间"""
        return datetime.fromtimestamp(self.time)


@dataclass
class PhotoDTO:
    """照片记录数据传输对象"""
    id: str = ""
    baby_id: str = ""
    time: float = 0.0
    note: Optional[str] = None
    has_picture: bool = False
    file_path: str = ""
    description: Optional[str] = None
    timestamp: float = field(default_factory=lambda: datetime.now().timestamp())
    
    @property
    def photo_time(self) -> datetime:
        """照片时间"""
        return datetime.fromtimestamp(self.time)


@dataclass
class VideoDTO:
    """视频记录数据传输对象"""
    id: str = ""
    baby_id: str = ""
    time: float = 0.0
    note: Optional[str] = None
    has_picture: bool = False
    file_path: str = ""
    duration: int = 0  # 秒
    description: Optional[str] = None
    timestamp: float = field(default_factory=lambda: datetime.now().timestamp())
    
    @property
    def video_time(self) -> datetime:
        """视频时间"""
        return datetime.fromtimestamp(self.time)
    
    @property
    def duration_minutes(self) -> float:
        """视频时长（分钟）"""
        return self.duration / 60.0
