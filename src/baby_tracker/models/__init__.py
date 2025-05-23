"""
Baby Tracker Models

这个包包含了所有的数据模型：
- SQLAlchemy ORM 模型：用于数据库操作
- Dataclass DTO：用于服务层和API层之间的数据传输
- 数据映射器：在ORM模型和DTO之间转换
"""

# SQLAlchemy ORM 模型 - 基础
from .base import BaseModel, TimestampMixin
from .baby import Baby

# 保持现有模型兼容性
from .feeding import Nursing, Formula
from .health import Sleep, Diaper
from .activity import Playtime, Bath
from .lookup import (
    SleepDesc, FeedDesc, DiaperDesc
)

# 新的 Dataclass DTO 和映射器
try:
    from .dto import (
        BabyDTO, NursingDTO, FormulaDTO, SleepDTO, DiaperDTO,
        WeightDTO, HeightDTO, TemperatureDTO, FeedingStatsDTO, GrowthStatsDTO,
        Gender, FinishSide
    )
    from .mappers import (
        BabyMapper, NursingMapper, FormulaMapper, SleepMapper,
        WeightMapper, TemperatureMapper
    )
    _HAS_DTO = True
except ImportError:
    _HAS_DTO = False

__all__ = [
    # 基础 ORM 模型
    "BaseModel", "TimestampMixin", "Baby",
    
    # 现有模型（保持兼容性）
    "Nursing", "Formula", 
    "Sleep", "Diaper", 
    "Playtime", "Bath",
    "SleepDesc", "FeedDesc", "DiaperDesc",
    "OtherActivityLocationSelection",
]

# 如果DTO可用，添加到导出列表
if _HAS_DTO:
    __all__.extend([
        # DTOs
        'BabyDTO', 'NursingDTO', 'FormulaDTO', 'SleepDTO', 'DiaperDTO',
        'WeightDTO', 'HeightDTO', 'TemperatureDTO', 'FeedingStatsDTO', 'GrowthStatsDTO',
        'Gender', 'FinishSide',
        
        # Mappers
        'BabyMapper', 'NursingMapper', 'FormulaMapper', 'SleepMapper',
        'WeightMapper', 'TemperatureMapper',
    ])
