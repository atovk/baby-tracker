"""
Baby Tracker 仓储层

这个包包含所有数据访问仓储：
- 基础仓储：通用仓储模式实现
- 宝宝仓储：宝宝实体的数据访问
- 喂养仓储：喂养记录相关数据访问
- 健康仓储：健康记录相关数据访问
- 活动仓储：活动记录相关数据访问
"""

try:
    from .base_repository import BaseRepository
    from .baby_repository import BabyRepository
    from .feeding_repository import NursingRepository, FormulaRepository, FeedingStatsRepository
    from .health_repository import (
        SleepRepository, DiaperRepository, WeightRepository, 
        HeightRepository, HeadRepository, TemperatureRepository
    )
    from .activity_repository import (
        PlaytimeRepository, BathRepository, PhotoRepository, VideoRepository
    )
    
    __all__ = [
        'BaseRepository',
        'BabyRepository',
        'NursingRepository',
        'FormulaRepository',
        'FeedingStatsRepository',
        'SleepRepository',
        'DiaperRepository',
        'WeightRepository',
        'HeightRepository',
        'HeadRepository',
        'TemperatureRepository',
        'PlaytimeRepository',
        'BathRepository',
        'PhotoRepository',
        'VideoRepository',
    ]
except ImportError:
    __all__ = []